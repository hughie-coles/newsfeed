#!/usr/bin/env python3
"""
filter_digest.py — tight-filter a Feed Digest data file down to Hughie's 4 buckets.

Slots into the daily routine BETWEEN fetch_feeds.py and build_digest.py:

    python3 fetch_feeds.py   --output digest.json
    python3 filter_digest.py --input  digest.json --output digest.json   # <-- new
    python3 build_digest.py  --input  digest.json --output digest.html

It reads digest.json, drops every article that doesn't clearly fit one of the
four buckets below, prunes now-empty categories, and writes the same JSON shape
back out — so build_digest.py keeps rendering exactly as before, just with fewer
items. No LLM, fully deterministic.

The filter is schema-agnostic: it walks the JSON, treats any dict that has both a
title-ish and a url-ish key as an "article", scores it, and keeps it or drops it.
Tune the four lists below to taste; re-run, eyeball the draft, adjust.
"""

import argparse
import json
import sys

# --- Tuning knobs -----------------------------------------------------------
# An article is KEPT if it is not hard-excluded AND scores >= MIN_SCORE.
# Scoring: +2 if its source is in INCLUDE_SOURCES, +1 per INCLUDE_KEYWORD hit in
# the title (capped at +2). Hard-exclude (source or keyword) always wins.

MIN_SCORE = 2

# Sources whose articles almost always fit (substring, case-insensitive).
INCLUDE_SOURCES = [
    "bytebytego", "system design newsletter", "pragmatic engineer",
    "david cummings", "lenny", "intercom", "cloudflare", "netflix tech",
    "airbnb engineering", "salesforce engineering", "stripe", "timescale",
    "tigerdata", "percona", "jack-vanlightly", "jack vanlightly", "confluent",
    "eli bendersky", "antirez", "stack overflow", "github engineering",
    "spotify", "martin fowler", "leaddev", "tim ferriss", "anca onuta",
    "codeopinion", "pinterest engineering", "grab", "doordash", "figma",
    "system design", "coding confessions", "digitalocean",
]

# Title keywords that signal one of the four buckets.
INCLUDE_KEYWORDS = [
    # 4) AI agents & applied LLMs
    "agent", "agents", "agentic", "llm", "llms", "rag", "mcp", "eval", "evals",
    "token", "context", "multi-agent", "inference", "vector", "embedding",
    "prompt", "fine-tun", "model serving", "model router",
    # 3) Infra & system design
    "postgres", "kafka", "database", "distributed", "scaling", "scale",
    "scaled", "observability", "latency", "throughput", "bandwidth", "deploy",
    "deployment", "infrastructure", "system design", "architecture",
    "event-driven", "partition", "cassandra", "clickhouse", "virtual memory",
    "page table", "performance", "real-time", "pipeline", "payment",
    # 2) SaaS product, growth, competitive intel
    "pricing", "packaging", "saas", "growth", "retention", " vs ", "comparison",
    "competitive", "revenue", "billing", "go-to-market", "gtm",
    # 1) Founders & strategy
    "founder", "founders", "startup", "fundrais", "vc", "venture", "series a",
    "entrepreneur", "solo found", "leadership", "customers",
]

# Hard-exclude: any source containing one of these is dropped outright.
EXCLUDE_SOURCES = [
    "the diplomat", "righto", "ken shirriff", "geldreich", "codename one",
    "hackaday",
]

# Hard-exclude: any title containing one of these is dropped outright.
EXCLUDE_KEYWORDS = [
    # low-level hardware / retro internals
    "cpu", "gpu", "fpga", "transistor", "8087", "retro", "commodore",
    "soldering", "oscilloscope", "satellite", "star tracker", "b-52",
    # graphics / game-engine / language internals
    "shader", "vulkan", "opengl", "directx", "d3d12", "raytrac", "ray tracing",
    "game engine", "sprite", "box2d", "wasm", "webassembly", "bc7",
    # security-breach / CVE news (keep architecture-of-security, drop news)
    "cve-", "ransomware", "phishing", "malware", "data breach", "0-day",
    "zero-day", "exploit chain",
    # politics / general news
    "geopolitic", "election", "tariff",
]

ARTICLE_LIST_KEYS = ("items", "articles", "entries", "posts", "links")
TITLE_KEYS = ("title", "headline", "name")
URL_KEYS = ("url", "link", "href")
SOURCE_KEYS = ("source", "feed", "blog", "site", "author", "publication")


def _first(d, keys):
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ""


def is_article(node):
    return (
        isinstance(node, dict)
        and _first(node, TITLE_KEYS)
        and _first(node, URL_KEYS)
    )


def keep_article(article):
    title = _first(article, TITLE_KEYS).lower()
    source = _first(article, SOURCE_KEYS).lower()
    blob = title + " " + source

    if any(s in source for s in EXCLUDE_SOURCES):
        return False
    if any(k in blob for k in EXCLUDE_KEYWORDS):
        return False

    score = 0
    if any(s in source for s in INCLUDE_SOURCES):
        score += 2
    kw_hits = sum(1 for k in INCLUDE_KEYWORDS if k in title)
    score += min(kw_hits, 2)
    return score >= MIN_SCORE


def _is_empty_category(node):
    """A dict that holds an (now-empty) article list and nothing else worth keeping."""
    if not isinstance(node, dict):
        return False
    for k in ARTICLE_LIST_KEYS:
        if k in node:
            v = node.get(k)
            if isinstance(v, list) and len(v) == 0:
                return True
    return False


def prune(node):
    if isinstance(node, list):
        out = []
        for x in node:
            if is_article(x):
                if keep_article(x):
                    out.append(x)
            else:
                px = prune(x)
                if px is None or _is_empty_category(px):
                    continue
                out.append(px)
        return out
    if isinstance(node, dict):
        return {k: prune(v) for k, v in node.items()}
    return node


def count_articles(node):
    if isinstance(node, list):
        return sum(count_articles(x) for x in node)
    if isinstance(node, dict):
        if is_article(node):
            return 1
        return sum(count_articles(v) for v in node.values())
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--min-score", type=int, default=MIN_SCORE)
    args = ap.parse_args()

    global MIN_SCORE
    MIN_SCORE = args.min_score

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    before = count_articles(data)
    filtered = prune(data)
    after = count_articles(filtered)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print(
        f"filter_digest: kept {after}/{before} articles "
        f"(dropped {before - after}, min_score={MIN_SCORE})",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
