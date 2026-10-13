# feed-digests

Weekly RSS feed digest pipeline. Personal productivity tool — optimize for reliability and readability.

## Pipeline

```
feeds.opml → fetch_feeds.py → YYYY-MM-DD.json → build_digest.py (AI summaries) → build_html.py → Gmail draft
```

## Key Files

- `feeds.opml` — ~1200+ RSS sources across categories (Engineering, AI/ML, Leadership, Daily aggregators, etc.)
- `fetch_feeds.py` — Fetches feeds concurrently (20 workers), filters last 7 days (168h), extracts articles from digest-style feeds, outputs JSON
- `build_digest.py` — Calls Claude Haiku API for 1-2 sentence summaries per article
- `build_html.py` / `build_html_compact.py` — Generates styled single-file HTML digest email
- `requirements.txt` — Python deps (feedparser)

## Running Locally

```bash
source .venv/bin/activate
python3 fetch_feeds.py                    # outputs ./YYYY-MM-DD.json
python3 build_digest.py                   # requires ANTHROPIC_API_KEY
python3 build_html.py                     # outputs HTML digest
```

`fetch_feeds.py` options: `--hours 168`, `--max-per-category 25`, `--output path`, `--no-extract-digests`

## Scheduled Trigger

Runs weekly, Monday 13:00 UTC, via Claude Code Remote (CCR). Clones repo fresh, runs pipeline, creates Gmail draft.

## Environment

- Python 3.12+ with venv at `.venv/`
- `ANTHROPIC_API_KEY` — required for AI summarization (falls back to excerpt)
- No test suite currently
