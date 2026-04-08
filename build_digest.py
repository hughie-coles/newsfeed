#!/usr/bin/env python3
"""Build daily digest HTML from JSON feed data with AI-generated summaries."""

import argparse
import json
import os
import sys
from datetime import datetime
from html import escape
from pathlib import Path

import anthropic

CATEGORY_COLORS = [
    "#4f46e5",  # indigo
    "#0891b2",  # cyan
    "#059669",  # emerald
    "#d97706",  # amber
    "#dc2626",  # red
    "#7c3aed",  # violet
    "#db2777",  # pink
    "#ea580c",  # orange
]


def cat_color(i):
    return CATEGORY_COLORS[i % len(CATEGORY_COLORS)]


def cat_id(cat):
    return cat.lower().replace(" ", "-").replace("/", "-")


def format_date(generated_at):
    """Parse generated_at from JSON and return a readable date string like 'Monday, April 7, 2026'."""
    try:
        dt = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        # Fallback: try just date portion
        try:
            dt = datetime.strptime(generated_at[:10], "%Y-%m-%d")
        except Exception:
            return generated_at
    return dt.strftime("%A, %B %-d, %Y")


def get_summary(client, title, excerpt):
    """Call Claude Haiku to generate a 1-2 sentence summary."""
    prompt = (
        "Given this article title and excerpt, write 1-2 sentences that tell the reader "
        "WHY they might want to click through — what is interesting or notable about this piece. "
        "Be specific and compelling, not generic. Write only the summary, no preamble.\n\n"
        f"Title: {title}\nExcerpt: {excerpt[:500]}"
    )
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()


def build_html(data, summaries_by_category, display_date):
    stats = data["stats"]
    categories = data["categories"]
    overflow = data.get("overflow", {})

    total_items = sum(len(v) for v in categories.values())
    cat_count = len(categories)
    feeds_checked = stats["total_feeds"]
    feeds_errored = stats["feeds_errored"]
    generated_at = data.get("generated_at", "")

    # --- TOC pills ---
    toc_pills = ""
    for i, cat in enumerate(categories.keys()):
        color = cat_color(i)
        anchor = cat_id(cat)
        count = len(categories[cat])
        toc_pills += (
            f'<a href="#{escape(anchor)}" style="display:inline-block;padding:5px 14px;'
            f'border-radius:20px;background:{color};color:#fff;text-decoration:none;'
            f'font-size:13px;font-weight:500;margin:4px 4px 4px 0;">'
            f'{escape(cat)} ({count})</a>\n'
        )

    # --- Category sections ---
    sections_html = ""
    for i, (cat, items) in enumerate(categories.items()):
        color = cat_color(i)
        anchor = cat_id(cat)

        items_html = ""
        for j, item in enumerate(items):
            title = item.get("title", "Untitled")
            link = item.get("link", "#")
            feed_name = item.get("feed_name", "")
            pub_date = item.get("published", "")
            summary = summaries_by_category.get(cat, {}).get(title, "")

            # Date formatting for individual items
            date_str = ""
            if pub_date:
                try:
                    dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                    date_str = dt.strftime("%b %-d")
                except Exception:
                    date_str = pub_date[:10] if len(pub_date) >= 10 else pub_date

            meta_parts = []
            if feed_name:
                meta_parts.append(escape(feed_name))
            if date_str:
                meta_parts.append(escape(date_str))
            meta_line = " &middot; ".join(meta_parts)

            border_bottom = "border-bottom:1px solid #f0f2f5;" if j < len(items) - 1 else ""

            items_html += (
                f'<div style="padding:14px 20px 14px 24px;border-left:4px solid {color};{border_bottom}">'
                f'<a href="{escape(link)}" target="_blank" rel="noopener" '
                f'style="display:block;font-weight:600;font-size:15px;color:#1a1a2e;text-decoration:none;margin-bottom:3px;">'
                f'{escape(title)}</a>'
                f'<div style="font-size:12px;color:#9ca3af;margin-bottom:6px;">{meta_line}</div>'
                f'<div style="font-size:14px;color:#4b5563;line-height:1.55;">{escape(summary)}</div>'
                f'</div>'
            )

        overflow_note = ""
        if cat in overflow:
            n = overflow[cat]
            overflow_note = (
                f'<div style="padding:10px 20px;font-size:13px;color:#6b7280;font-style:italic;'
                f'border-top:1px dashed #e0e0e0;background:#fafafa;">'
                f'+{n} more items not shown</div>'
            )

        sections_html += (
            f'<table cellpadding="0" cellspacing="0" border="0" width="100%" '
            f'style="background:#fff;border-radius:8px;margin-bottom:20px;'
            f'box-shadow:0 1px 3px rgba(0,0,0,0.08);overflow:hidden;">'
            f'<tr><td id="{escape(anchor)}" style="background:{color};padding:14px 20px;'
            f'font-size:16px;font-weight:700;color:#fff;">'
            f'{escape(cat)}'
            f'<span style="font-size:12px;font-weight:500;opacity:0.85;'
            f'background:rgba(255,255,255,0.2);padding:2px 9px;border-radius:999px;'
            f'margin-left:10px;">{len(items)} items</span>'
            f'</td></tr>'
            f'<tr><td style="padding:0;">{items_html}</td></tr>'
            f'{f"<tr><td>{overflow_note}</td></tr>" if overflow_note else ""}'
            f'</table>\n'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feed Digest: {escape(display_date)}</title>
</head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;background:#f0f2f5;color:#222;font-size:15px;line-height:1.6;margin:0;padding:0;">
<div style="max-width:720px;margin:0 auto;padding:0 16px 48px;">

  <!-- Header -->
  <div style="background-color:#1a1a2e;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#fff;padding:36px 24px 28px;margin-bottom:24px;border-radius:0 0 8px 8px;">
    <div style="font-size:26px;font-weight:700;letter-spacing:-0.5px;">Feed Digest</div>
    <div style="font-size:15px;opacity:0.7;margin-top:4px;">{escape(display_date)}</div>
    <div style="display:flex;gap:24px;margin-top:16px;flex-wrap:wrap;">
      <div style="text-align:center;">
        <div style="font-size:24px;font-weight:700;color:#60a5fa;">{total_items}</div>
        <div style="font-size:11px;opacity:0.7;text-transform:uppercase;letter-spacing:0.5px;">Items</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:24px;font-weight:700;color:#34d399;">{stats['feeds_fetched']}</div>
        <div style="font-size:11px;opacity:0.7;text-transform:uppercase;letter-spacing:0.5px;">Feeds</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:24px;font-weight:700;color:#f472b6;">{cat_count}</div>
        <div style="font-size:11px;opacity:0.7;text-transform:uppercase;letter-spacing:0.5px;">Categories</div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:24px;font-weight:700;color:#fbbf24;">{stats['total_feeds']}</div>
        <div style="font-size:11px;opacity:0.7;text-transform:uppercase;letter-spacing:0.5px;">Checked</div>
      </div>
    </div>
  </div>

  <!-- TOC -->
  <div style="background:#fff;border-radius:8px;padding:16px 20px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.08);">
    <div style="font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#9ca3af;margin-bottom:10px;font-weight:600;">Categories</div>
    <div>{toc_pills}</div>
  </div>

  <!-- Sections -->
  {sections_html}

  <!-- Footer -->
  <div style="text-align:center;font-size:12px;color:#aaa;padding:16px 0;">
    {feeds_checked} feeds checked &bull; {feeds_errored} unreachable &bull; generated {escape(generated_at)}
  </div>

</div>
</body>
</html>"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build daily digest HTML from JSON feed data with AI-generated summaries."
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to the input JSON file (e.g. 2026-04-07.json)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Path for the output HTML file. Default: same directory/basename as input with .html extension"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")

    with open(input_path) as f:
        data = json.load(f)

    # Format display date from generated_at
    generated_at = data.get("generated_at", "")
    display_date = format_date(generated_at)

    # Set up Anthropic client
    token_file = "/home/claude/.claude/remote/.session_ingress_token"
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key and os.path.exists(token_file):
        api_key = Path(token_file).read_text().strip()

    use_api = bool(api_key)
    client = None
    if use_api:
        os.environ["ANTHROPIC_API_KEY"] = api_key
        client = anthropic.Anthropic()
        # Quick connectivity test
        try:
            client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=5,
                messages=[{"role": "user", "content": "ping"}]
            )
            print("Claude API: connected")
        except Exception as e:
            print(f"Claude API unavailable ({e}), using excerpt fallback")
            use_api = False
            client = None

    summaries_by_category = {}
    total_summarized = 0

    for cat, items in data["categories"].items():
        summaries_by_category[cat] = {}
        for item in items:
            title = item["title"]
            excerpt = item.get("excerpt", "")
            if use_api:
                try:
                    summary = get_summary(client, title, excerpt)
                except Exception as e:
                    print(f"  Summary error for '{title[:50]}': {e}")
                    summary = excerpt[:220].rstrip() + ("\u2026" if len(excerpt) > 220 else "")
            else:
                summary = excerpt[:220].rstrip() + ("\u2026" if len(excerpt) > 220 else "")
            summaries_by_category[cat][title] = summary
            total_summarized += 1
            print(f"  [{cat}] {title[:70]}")

    print(f"\nSummarized {total_summarized} items across {len(data['categories'])} categories.")

    html = build_html(data, summaries_by_category, display_date)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML written: {output_path} ({len(html):,} bytes)")
    return total_summarized, len(data["categories"])


if __name__ == "__main__":
    total, cats = main()
    print(f"\nDone: {total} items, {cats} categories")
