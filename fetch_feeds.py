#!/usr/bin/env python3
"""Fetch RSS feeds from an OPML file and output recent items as JSON."""

import argparse
import concurrent.futures
import json
import re
import socket
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import feedparser


def resolve_entry_link(entry, feed_url):
    """Prefer the alternate HTML link from entry.links over entry.link.

    Returns "" if the resolved link matches the feed URL itself.
    """
    best = ""
    alt_no_type = ""
    for link_obj in entry.get("links", []):
        if link_obj.get("rel") == "alternate":
            ltype = link_obj.get("type", "")
            if "html" in ltype:
                best = link_obj.get("href", "")
                break
            elif not ltype and not alt_no_type:
                alt_no_type = link_obj.get("href", "")
    if not best:
        best = alt_no_type or entry.get("link", "")
    # Skip if the resolved link is really just the feed URL
    if best:
        parsed_best = urlparse(best)
        parsed_feed = urlparse(feed_url)
        clean_best = f"{parsed_best.scheme}://{parsed_best.netloc}{parsed_best.path}".rstrip("/")
        clean_feed = f"{parsed_feed.scheme}://{parsed_feed.netloc}{parsed_feed.path}".rstrip("/")
        if clean_best == clean_feed:
            return ""
    return best


def parse_opml(opml_path):
    """Parse OPML file, return list of {url, name, category} dicts."""
    tree = ET.parse(opml_path)
    root = tree.getroot()
    body = root.find("body")
    feeds = []

    for outline in body:
        if outline.get("type") == "rss":
            feeds.append({
                "url": outline.get("xmlUrl"),
                "html_url": outline.get("htmlUrl", ""),
                "name": outline.get("text", "Unknown"),
                "category": "Uncategorized",
            })
        elif len(outline):
            category = outline.get("text", "Uncategorized")
            for child in outline:
                if child.get("type") == "rss":
                    feeds.append({
                        "url": child.get("xmlUrl"),
                        "html_url": child.get("htmlUrl", ""),
                        "name": child.get("text", "Unknown"),
                        "category": category,
                    })

    return feeds


def strip_html(text):
    """Remove HTML tags and collapse whitespace."""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def parse_date(entry):
    """Extract a timezone-aware datetime from a feed entry, or None."""
    for field in ("published_parsed", "updated_parsed"):
        t = entry.get(field)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except (ValueError, TypeError):
                continue
    # Fallback: try parsing the raw date string directly
    for field in ("published", "updated"):
        raw = entry.get(field, "")
        if not raw:
            continue
        # Strip non-standard timezone suffixes like "GMT-8"
        cleaned = re.sub(r"GMT[+-]\d+$", "GMT", raw.strip())
        for fmt in (
            "%a, %d %b %Y %H:%M:%S %Z",
            "%a, %d %b %Y %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
        ):
            try:
                dt = datetime.strptime(cleaned, fmt)
                return dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
    return None


class LinkExtractor(HTMLParser):
    """Extract <a> tags from HTML content with surrounding block context."""

    BLOCK_TAGS = {"p", "li", "div", "td", "th", "blockquote", "dd", "dt", "h1",
                  "h2", "h3", "h4", "h5", "h6", "article", "section"}

    def __init__(self):
        super().__init__()
        self.links = []
        self._current_href = None
        self._current_text = []
        self._block_text = []
        self._block_links = []
        self._in_block = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCK_TAGS:
            # Innermost block wins: reset context on each new block open.
            # This means nested blocks discard outer context, which is fine
            # for the flat structure of digest HTML (sibling <p>/<li> tags).
            self._in_block += 1
            self._block_text = []
            self._block_links = []
        if tag == "a":
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", "")
            if href and href.startswith("http"):
                self._current_href = href
                self._current_text = []

    def handle_data(self, data):
        if self._current_href is not None:
            self._current_text.append(data)
        if self._in_block > 0:
            self._block_text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._current_href:
            text = " ".join("".join(self._current_text).split()).strip()
            if text and len(text) > 3:
                link_entry = {"title": text, "link": self._current_href}
                self.links.append(link_entry)
                if self._in_block > 0:
                    self._block_links.append(link_entry)
            self._current_href = None
            self._current_text = []
        if tag in self.BLOCK_TAGS and self._in_block > 0:
            context = " ".join("".join(self._block_text).split()).strip()
            if context:
                for link_entry in self._block_links:
                    link_entry["context"] = context
            self._block_links = []
            self._block_text = []
            self._in_block -= 1


NOISE_DOMAINS = {
    "twitter.com", "x.com", "facebook.com", "linkedin.com", "reddit.com",
    "news.ycombinator.com", "youtube.com", "youtu.be", "instagram.com",
    "threads.net", "bsky.app", "mastodon.social",
}


def build_domain_category_map(feeds):
    """Map feed domains to their OPML categories, excluding Daily."""
    domain_map = {}
    for f in feeds:
        if f["category"] == "Daily":
            continue
        domain = urlparse(f["url"]).netloc.replace("www.", "")
        if domain and domain not in domain_map:
            domain_map[domain] = f["category"]
        html_url = f.get("html_url", "")
        if html_url:
            html_domain = urlparse(html_url).netloc.replace("www.", "")
            if html_domain and html_domain not in domain_map:
                domain_map[html_domain] = f["category"]
    return domain_map


def extract_digest_links(html_content, digest_url):
    """Extract individual article links from digest HTML content."""
    digest_domain = urlparse(digest_url).netloc.replace("www.", "")

    parser = LinkExtractor()
    parser.feed(html_content)

    results = []
    seen = set()
    for link in parser.links:
        url = link["link"].split("?")[0].split("#")[0].rstrip("/")
        domain = urlparse(link["link"]).netloc.replace("www.", "")
        if domain == digest_domain:
            continue
        if domain in NOISE_DOMAINS:
            continue
        if url in seen:
            continue
        seen.add(url)
        results.append({
            "title": link["title"],
            "link": link["link"],
            "context": link.get("context", "")[:300],
        })
    return results


def process_digests(categories, feeds):
    """Extract links from Daily digest articles and distribute to categories."""
    daily_items = categories.get("Daily", [])
    if not daily_items:
        return 0

    domain_map = build_domain_category_map(feeds)

    existing_urls = set()
    for cat_items in categories.values():
        for item in cat_items:
            normalized = item["link"].split("?")[0].split("#")[0].rstrip("/")
            existing_urls.add(normalized)

    extracted_count = 0
    for source_item in daily_items:
        content_html = source_item.get("_content_html", "")
        if not content_html:
            continue
        links = extract_digest_links(content_html, source_item["link"])
        for link in links:
            normalized = link["link"].split("?")[0].split("#")[0].rstrip("/")
            if normalized in existing_urls:
                continue
            existing_urls.add(normalized)

            link_domain = urlparse(link["link"]).netloc.replace("www.", "")
            category = domain_map.get(link_domain, "Daily")

            new_item = {
                "title": link["title"],
                "link": link["link"],
                "published": None,
                "excerpt": link.get("context", ""),
                "feed_name": source_item["feed_name"],
                "category": category,
            }
            if category not in categories:
                categories[category] = []
            categories[category].append(new_item)
            extracted_count += 1

    # Remove original digest articles and strip _content_html
    if "Daily" in categories:
        del categories["Daily"]
    for cat_items in categories.values():
        for item in cat_items:
            item.pop("_content_html", None)

    return extracted_count


def _title_words(title):
    """Normalize title to a set of significant words (>3 chars)."""
    words = re.sub(r"[^\w\s]", "", title.lower()).split()
    return {w for w in words if len(w) > 3}


TITLE_SIMILARITY_THRESHOLD = 0.6


def _titles_similar(words_a, words_b, threshold=TITLE_SIMILARITY_THRESHOLD):
    """Return True if two title word-sets share >= threshold of their words."""
    if not words_a or not words_b:
        return False
    union = len(words_a | words_b)
    if union == 0:
        return False
    return len(words_a & words_b) / union >= threshold


def deduplicate_by_title(categories):
    """Remove near-duplicate articles by title similarity.

    Within each category: keep the article with the longer excerpt.
    Across categories: keep the article in the category where it appeared first
    (OPML-sourced categories come before Daily-extracted ones).
    """
    # Within-category dedup
    for cat, items in list(categories.items()):
        word_sets = [_title_words(item["title"]) for item in items]
        remove = set()
        for i in range(len(items)):
            if i in remove:
                continue
            for j in range(i + 1, len(items)):
                if j in remove:
                    continue
                if _titles_similar(word_sets[i], word_sets[j]):
                    # Keep the one with longer excerpt
                    if len(items[i].get("excerpt", "")) >= len(items[j].get("excerpt", "")):
                        remove.add(j)
                    else:
                        remove.add(i)
                        break  # i is removed, stop comparing from i
        if remove:
            categories[cat] = [item for idx, item in enumerate(items) if idx not in remove]

    # Cross-category dedup: flatten with category order, first appearance wins
    seen = []  # list of (word_set, cat, idx)
    removals = {}  # {cat: set of indices to remove}
    for cat, items in categories.items():
        for idx, item in enumerate(items):
            ws = _title_words(item["title"])
            if not ws:
                continue
            duplicate = False
            for seen_ws, seen_cat, _seen_idx in seen:
                if _titles_similar(ws, seen_ws):
                    duplicate = True
                    break
            if duplicate:
                removals.setdefault(cat, set()).add(idx)
            else:
                seen.append((ws, cat, idx))

    for cat, indices in removals.items():
        categories[cat] = [item for idx, item in enumerate(categories[cat]) if idx not in indices]

    # Remove empty categories
    for cat in [c for c, items in categories.items() if not items]:
        del categories[cat]


def fetch_single_feed(feed, cutoff):
    """Fetch one feed, return (items_list, error_dict_or_None)."""
    url = feed["url"]
    name = feed["name"]
    category = feed["category"]

    try:
        d = feedparser.parse(url, request_headers={"User-Agent": "FeedDigest/1.0"})
        if d.bozo and not d.entries:
            return [], {"feed": name, "url": url, "error": str(d.bozo_exception)}

        items = []
        skipped_feed_links = 0
        for entry in d.entries:
            pub_dt = parse_date(entry)
            if not pub_dt or pub_dt < cutoff:
                continue

            content_html = ""
            content_list = entry.get("content", [])
            if content_list:
                content_html = content_list[0].get("value", "")
            raw_summary = content_html or entry.get("summary") or entry.get("description") or ""
            excerpt = strip_html(raw_summary)[:500]

            article_link = resolve_entry_link(entry, url)
            if not article_link:
                skipped_feed_links += 1
                continue

            item = {
                "title": entry.get("title", "Untitled"),
                "link": article_link,
                "published": pub_dt.isoformat() if pub_dt else None,
                "excerpt": excerpt,
                "feed_name": name,
                "category": category,
            }
            if category == "Daily" and content_html:
                item["_content_html"] = content_html
            items.append(item)

        if skipped_feed_links:
            print(f"  {name}: skipped {skipped_feed_links} entries (link matched feed URL)", file=sys.stderr)
        return items, None

    except Exception as e:
        return [], {"feed": name, "url": url, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Fetch RSS feeds from OPML")
    parser.add_argument("--opml", default=str(Path(__file__).parent / "feeds.opml"),
                        help="Path to OPML file")
    parser.add_argument("--hours", type=int, default=24,
                        help="Look back N hours (default: 24)")
    parser.add_argument("--max-per-category", type=int, default=25,
                        help="Max items per category (default: 25, 0=unlimited)")
    parser.add_argument("--no-extract-digests", action="store_true",
                        help="Disable digest article extraction")
    parser.add_argument("--output", default=None,
                        help="Output JSON path (default: ~/feed-digests/YYYY-MM-DD.json)")
    args = parser.parse_args()

    socket.setdefaulttimeout(10)

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=args.hours)

    feeds = parse_opml(args.opml)
    print(f"Parsed {len(feeds)} feeds from OPML", file=sys.stderr)

    all_items = []
    all_errors = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_feed = {
            executor.submit(fetch_single_feed, f, cutoff): f for f in feeds
        }
        done = 0
        for future in concurrent.futures.as_completed(future_to_feed):
            done += 1
            if done % 50 == 0:
                print(f"  Fetched {done}/{len(feeds)}...", file=sys.stderr)
            items, error = future.result()
            all_items.extend(items)
            if error:
                all_errors.append(error)

    # Group by category
    categories = {}
    for item in all_items:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    # Extract links from digest articles
    digest_extracted = 0
    if not args.no_extract_digests:
        print("Extracting links from Daily digest articles...", file=sys.stderr)
        digest_extracted = process_digests(categories, feeds)
        print(f"  Extracted {digest_extracted} articles from digests", file=sys.stderr)

    # Deduplicate near-identical titles within and across categories
    pre_dedup = sum(len(v) for v in categories.values())
    deduplicate_by_title(categories)
    post_dedup = sum(len(v) for v in categories.values())
    if pre_dedup != post_dedup:
        print(f"  Deduplication removed {pre_dedup - post_dedup} articles", file=sys.stderr)

    # Sort items within each category by date (newest first), undated at the end
    for cat in categories:
        categories[cat].sort(
            key=lambda x: x["published"] or "0000", reverse=True
        )

    # Trim to max per category
    overflow = {}
    if args.max_per_category > 0:
        for cat in categories:
            if len(categories[cat]) > args.max_per_category:
                overflow[cat] = len(categories[cat]) - args.max_per_category
                categories[cat] = categories[cat][:args.max_per_category]

    result = {
        "generated_at": now.isoformat(),
        "cutoff_time": cutoff.isoformat(),
        "stats": {
            "total_feeds": len(feeds),
            "feeds_fetched": len(feeds) - len(all_errors),
            "feeds_errored": len(all_errors),
            "total_items": len(all_items),
            "digest_articles_extracted": digest_extracted,
            "categories_with_items": len(categories),
        },
        "categories": categories,
        "overflow": overflow,
        "errors": all_errors,
    }

    output_path = args.output or str(
        Path(__file__).parent / f"{now.strftime('%Y-%m-%d')}.json"
    )
    Path(output_path).write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nDone! {len(all_items)} items from {len(feeds) - len(all_errors)} feeds "
          f"({len(all_errors)} errors). Saved to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
