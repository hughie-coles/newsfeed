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
from pathlib import Path

import feedparser


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
                "name": outline.get("text", "Unknown"),
                "category": "Uncategorized",
            })
        elif len(outline):
            category = outline.get("text", "Uncategorized")
            for child in outline:
                if child.get("type") == "rss":
                    feeds.append({
                        "url": child.get("xmlUrl"),
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
    return None


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
        for entry in d.entries:
            pub_dt = parse_date(entry)
            if pub_dt and pub_dt < cutoff:
                continue

            raw_summary = entry.get("summary") or entry.get("description") or ""
            excerpt = strip_html(raw_summary)[:500]

            items.append({
                "title": entry.get("title", "Untitled"),
                "link": entry.get("link", ""),
                "published": pub_dt.isoformat() if pub_dt else None,
                "excerpt": excerpt,
                "feed_name": name,
                "category": category,
            })

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
