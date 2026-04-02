#!/usr/bin/env python3
"""Build HTML digest from JSON feed data with AI-generated summaries."""

import json
from pathlib import Path
from html import escape

DATE = "2026-04-02"

with open(f"/home/user/newsfeed/{DATE}.json") as f:
    data = json.load(f)

stats = data["stats"]
overflow = data["overflow"]
errors = data["errors"]

# --- AI-generated summaries (keyed by category + index) ---
SUMMARIES = {
    "Politics": [
        "Former U.S. Ambassador Sam Brownback makes an urgent argument in the WSJ: without American engagement, Syria's religious minorities face violence that could destabilize any hope of democratic transition.",
        "Kyrgyzstan's once-untouchable security chief has been arrested in a major corruption case, signaling a dramatic and potentially destabilizing political rupture at the top of government.",
        "Nearly a decade in, Bangladesh's efforts to repatriate Rohingya refugees have produced almost nothing — this piece examines why diplomacy keeps failing and what, if anything, can break the deadlock.",
        "Nicholas Niarchos explores how China's grip on Congo's cobalt supply has become a geopolitical lever in the global race for battery technology dominance.",
        "With the Strait of Hormuz closed amid the Iran-US conflict, global energy trade is being rerouted — and Kazakhstan is emerging as a surprising new supplier and regional beneficiary.",
        "Seoul faces real pressure to commit naval forces to the Strait of Hormuz; this analysis lays out three strategic options and their tradeoffs for South Korea's delicate foreign policy balancing act.",
        "A nuanced take arguing China isn't simply 'exporting authoritarianism' to Central America — it's reinforcing existing antidemocratic trends, a distinction that matters for how to respond.",
        "The split between Kyrgyzstan's two most powerful political figures is compared to a high-stakes divorce — read this for expert context on what it means for the country's near-term stability.",
        "Indonesia weighs withdrawal from Lebanon peacekeeping under US and Israeli pressure, but analysts argue doing so would damage Jakarta's credibility and deliver a win to the powers it publicly opposes.",
    ],
    "Leadership": [
        "A sharp April Fools satire arguing 'doing nothing' is the hottest new innovation trend — worth a quick read as a wry antidote to relentless disruption culture.",
        "A practical guide arguing courage is the often-overlooked prerequisite for achieving any meaningful goal, with concrete steps for building it deliberately rather than waiting for it to appear.",
        "Despite the hype, human developers remain central to software development — this piece examines the real-world technical and organizational limits that keep AI coding tools from going further.",
        "Concrete strategies for tech leads drowning in competing demands and context-switching overhead, helping you reclaim focus and reduce the coordination tax of the role.",
    ],
    "Agile": [
        "A playful but insightful quiz to identify your default leadership instinct under pressure, then connect it to what agile teams actually need from a leader in those moments.",
        "A technical guide to designing resilient n8n automation workflows with error-first architecture and Claude as an AI decision node — useful for founders automating without a dedicated engineering team.",
        "A short community-supported reflection on what it actually means to be an agile coach, for anyone wrestling with that role's often-blurry boundaries and identity.",
    ],
    "Daily": [
        "Richard Seroter's curated links cover the current state of Java, uncomfortable truths about AI coding agents, and the uncertain outlook for junior developers — a compact digest worth scanning.",
        "Bruce Lawson's personal retrospective on Apple's 50th anniversary picks five standout moments from a long career watching the company evolve — nostalgic, opinionated, and fun.",
    ],
    "Engineering": [
        "Written by someone with an admitted 'one-sided beef' with Microsoft, this Power Automate guide is unusually honest — which makes it a trustworthy overview of what the platform actually does well.",
        "The latest monthly release of Microsoft's Python and Jupyter extensions for VS Code brings new features worth checking if these tools are part of your daily workflow.",
        "Draws on Marty Cagan's Inspired to explain why features built without deep customer knowledge get ignored, and what better epistemics in product design actually look like.",
        "A live stream tour of multi-tenancy features across the full .NET Critter Stack — the author claims it's the most complete multi-tenancy solution available in the ecosystem.",
        "AI without context produces noise, not signal — this piece makes the case for context-first AI strategy in go-to-market, explaining why most AI GTM efforts fall flat.",
        "Step-by-step guide to giving Claude Code real browser control on Linux with Wayland — enabling screenshots, clicks, and navigation that agents can act on.",
        "New Percona PostgreSQL operator defaults to PostgreSQL 18 and adds PVC snapshot backups and LDAP support — relevant if you're running Postgres on Kubernetes.",
        "Brings Rails upgrade diffs directly into your AI coding session via MCP, eliminating the browser tab-switching that slows down version migrations.",
        "A historical roundup of the most notable frontend April Fools pranks, including several that crossed the line and backfired badly — entertaining and occasionally cautionary.",
        "A brilliantly deadpan April Fools piece proposing a CSS API for smell-based user experiences — funny satire of spec culture even if you're not deep into CSS.",
        "Hard benchmark data comparing MySQL's MyRocks and InnoDB storage engines when RAM is tight — read this before choosing a storage engine for memory-constrained deployments.",
        "A practical Python project walkthrough: bulk-deleting 11,000+ Blogger spam comments using a script pair-coded with Claude — useful both as a script and as an AI collaboration case study.",
        "Aceto solves a real AI agent pain point: giving agents visual context about HTML mockups so you can say 'change this element' without resorting to long text descriptions.",
        "Argues that ad-hoc AI use by developers is a business reliability risk, and that spec-driven methodology is how teams get consistent, accountable AI-assisted delivery.",
        "Andrew Lock explains a niche but useful .NET options package for request-scoped configuration — with an honest verdict on when it's actually worth reaching for.",
        "How to use OpenTelemetry to get a real-time, fleet-wide inventory of which .NET runtime versions are actually running in production — surprisingly hard to answer without this.",
        "Shows how to build an always-on AI assistant reachable via WhatsApp, Telegram, or Slack using Zapier MCP, with safety guardrails built into the architecture.",
        "Zapier's accessible guide for non-technical teams wanting to automate workflows with AI — written specifically for people who tune out jargon and just want things to work.",
        "Nine ready-to-use Python automation scripts covering common pain points like data entry, file management, and batch processing — practical and immediately usable.",
        "Zapier's 2026 roundup of the best AI image generation tools — useful for anyone evaluating the landscape after years of rapid development and new entrants.",
        "Toady One shares progress on magical populations and worldgen infrastructure in Dwarf Fortress — essential reading for fans tracking the ongoing development of this legendary game.",
        "The April 2026 dev log plus the Future of the Fortress Q&A from Toady One, covering the latest direction and upcoming features for Dwarf Fortress.",
        "Uses pop-culture references to introduce Example Mapping, a collaborative technique for clarifying requirements before writing code — accessible even if the jokes don't land.",
        "An AI skeptic's honest assessment of using GenAI as an interactive rubber duck for debugging — when it genuinely helps, when it doesn't, and why the distinction matters.",
        "A provocative piece arguing the real revelation from LLMs isn't the end of coding — it's how many developers secretly don't enjoy it, and what that means for the industry.",
    ],
    "Engineering Blogs": [
        "Action required for Wear OS developers: the 64-bit mandate is coming, and this guide from Google explains exactly what changes are needed to your apps and when.",
        "Telerik's ThemeBuilder now offers centralized font management and AI-assisted component theming, streamlining the design-to-code workflow for teams using their tools.",
        "A practical guide to WCAG-compliant accessibility in Angular using production-ready directives — get accessible components without rolling your own ARIA implementation.",
        "AWS presents a reference architecture using fixed cameras and generative AI for near-real-time safety hazard detection — concrete and applicable to industrial or warehouse environments.",
        "A frank argument that most MongoDB pain points are workload mismatch problems that follow you to Postgres too — read this before committing to a database migration.",
        "Temporary AWS credential delegation for HCP Terraform is now generally available, simplifying cloud setup while improving security governance for AWS-heavy organizations.",
        "HCP Terraform can now restrict API token acceptance to predefined IP addresses — a straightforward but meaningful security upgrade for organizations with strict network controls.",
        "While the industry races to replace headcount with AI agents, Udacity is rolling out a different approach starting today — worth reading to understand the alternative thesis.",
        "Real Python's comprehensive guide to Python classes covering attributes, methods, and inheritance — a solid reference or refresher whether you're learning OOP or need a quick review.",
        "Eight years in, Cloudflare's latest independent privacy audit of 1.1.1.1 shows the protections are actually working — reassuring reading if you recommend or use this resolver.",
        "Cloudflare launches EmDash, a CMS that runs plugins in sandboxed Workers, directly attacking WordPress's longstanding plugin security nightmare with a modern architecture.",
        "Real Python's interactive quiz on Python keywords, including the tricky distinction between regular and soft keywords — good for testing your knowledge of the edges.",
        "Ably explains how channel-based architecture decouples AI session state from the transport layer, enabling chat sessions that survive device switches without losing context.",
        "Jeremy Kun's annual April Cools piece reviews Ben Recht's book on how AI systems came to make 'irrational' decisions — an unusual and likely thought-provoking read for ML practitioners.",
        "High-quality local text-to-speech is now genuinely viable on CPU without sacrificing privacy — Kokoro may be the tool you've been waiting for if you need on-device TTS.",
        "Snyk shares five hard-won lessons from building AI security tooling with design partners, covering AI discovery, risk intelligence, and policy automation for governing AI sprawl.",
        "Khan Academy's account of moving their mobile apps to React Native — real lessons from a production migration at meaningful scale, worth reading before undertaking your own.",
        "Engineering lessons from surviving a sudden 2.5x traffic spike in one week — a genuinely instructive scaling story from Khan Academy with takeaways applicable to most systems.",
        "How Khan Academy manages Go microservices in a single large monorepo — honest discussion of the tradeoffs for teams weighing the same architectural decision.",
        "Practical strategies for upgrading hundreds of React components without breaking production — essential reading for any team sitting on significant UI technical debt.",
        "Khan Academy on how making engineering principles explicit helped guide scaling decisions and team growth — useful framing for any engineering org trying to scale culture alongside systems.",
        "A practical guide to an often-neglected accessibility requirement: ensuring your web app remains usable and navigable under Windows High Contrast Mode.",
        "Khan Academy's guide to picking up Kotlin if you're coming from Python — useful for teams considering or currently undergoing a language transition on the server side.",
        "How Khan Academy uses static analysis across a polyglot codebase to catch bugs early and enforce safety invariants — a good model for teams working across multiple languages.",
        "Why and how Khan Academy moved server-side code to Kotlin, with practical lessons and honest reflection for any team evaluating the same move.",
    ],
}

CATEGORY_COLORS = {
    "Politics": "#e74c3c",
    "Leadership": "#3498db",
    "Agile": "#27ae60",
    "Daily": "#f39c12",
    "Engineering": "#8e44ad",
    "Engineering Blogs": "#16a085",
}

DEFAULT_COLORS = ["#e67e22", "#1abc9c", "#c0392b", "#2980b9", "#d35400", "#7f8c8d"]

def cat_color(cat, idx):
    return CATEGORY_COLORS.get(cat, DEFAULT_COLORS[idx % len(DEFAULT_COLORS)])

def cat_id(cat):
    return cat.lower().replace(" ", "-").replace("/", "-")

categories = data["categories"]
total_items = sum(len(v) for v in categories.values())

# Build HTML
lines = []

lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feed Digest: 2026-04-02</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: #f0f2f5;
    color: #222;
    font-size: 15px;
    line-height: 1.6;
  }
  a { color: inherit; }
  .wrapper { max-width: 720px; margin: 0 auto; padding: 0 16px 48px; }

  /* Header */
  .header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
    padding: 36px 24px 28px;
    margin-bottom: 24px;
  }
  .header h1 { font-size: 1.7rem; font-weight: 700; letter-spacing: -0.5px; }
  .header .date { font-size: 0.95rem; opacity: 0.7; margin-top: 4px; }
  .header .stats { display: flex; gap: 20px; margin-top: 16px; flex-wrap: wrap; }
  .header .stat { text-align: center; }
  .header .stat .num { font-size: 1.5rem; font-weight: 700; }
  .header .stat .lbl { font-size: 0.75rem; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.5px; }

  /* TOC */
  .toc {
    background: #fff;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  .toc h2 { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-bottom: 12px; }
  .toc-pills { display: flex; flex-wrap: wrap; gap: 8px; }
  .toc-pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    color: #fff;
    text-decoration: none;
    font-size: 0.82rem;
    font-weight: 500;
  }
  .toc-pill:hover { opacity: 0.85; }

  /* Category sections */
  .cat-section {
    background: #fff;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    overflow: hidden;
  }
  .cat-header {
    padding: 14px 20px;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .cat-count {
    font-size: 0.75rem;
    font-weight: 500;
    opacity: 0.85;
    background: rgba(255,255,255,0.2);
    padding: 2px 9px;
    border-radius: 999px;
  }
  .cat-items { }
  .item {
    padding: 14px 20px 14px 24px;
    border-left: 4px solid transparent;
    border-bottom: 1px solid #f0f2f5;
  }
  .item:last-child { border-bottom: none; }
  .item-title {
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    color: #1a1a2e;
    display: block;
    margin-bottom: 3px;
  }
  .item-title:hover { text-decoration: underline; }
  .item-source {
    font-size: 0.75rem;
    color: #999;
    margin-bottom: 6px;
  }
  .item-summary {
    font-size: 0.85rem;
    color: #444;
    line-height: 1.55;
  }
  .overflow-note {
    padding: 10px 20px;
    font-size: 0.8rem;
    color: #888;
    font-style: italic;
    border-top: 1px dashed #e0e0e0;
    background: #fafafa;
  }

  /* Footer */
  .footer {
    text-align: center;
    font-size: 0.8rem;
    color: #aaa;
    padding: 16px 0;
  }
</style>
</head>
<body>
<div class="header">
  <div class="wrapper" style="padding-bottom:0;">
    <h1>Feed Digest</h1>
    <div class="date">Thursday, April 2, 2026 &mdash; last 24 hours</div>
    <div class="stats">
""")

lines.append(f'      <div class="stat"><div class="num">{total_items}</div><div class="lbl">Items</div></div>')
lines.append(f'      <div class="stat"><div class="num">{stats["feeds_fetched"]}</div><div class="lbl">Feeds</div></div>')
lines.append(f'      <div class="stat"><div class="num">{len(categories)}</div><div class="lbl">Categories</div></div>')
lines.append(f'      <div class="stat"><div class="num">{stats["total_feeds"]}</div><div class="lbl">Checked</div></div>')

lines.append("""    </div>
  </div>
</div>
<div class="wrapper">
""")

# TOC
lines.append('<nav class="toc"><h2>Categories</h2><div class="toc-pills">')
for i, cat in enumerate(categories):
    color = cat_color(cat, i)
    cid = cat_id(cat)
    count = len(categories[cat])
    lines.append(f'<a class="toc-pill" href="#{cid}" style="background:{color};">{escape(cat)} ({count})</a>')
lines.append('</div></nav>')

# Category sections
for i, (cat, items) in enumerate(categories.items()):
    color = cat_color(cat, i)
    cid = cat_id(cat)
    summaries = SUMMARIES.get(cat, [])
    count = len(items)

    lines.append(f'<section class="cat-section" id="{cid}">')
    lines.append(f'<div class="cat-header" style="background:{color};">{escape(cat)}<span class="cat-count">{count} items</span></div>')
    lines.append('<div class="cat-items">')

    for j, item in enumerate(items):
        summary = summaries[j] if j < len(summaries) else ""
        title = escape(item.get("title", "Untitled"))
        link = item.get("link", "#")
        feed_name = escape(item.get("feed_name", ""))

        lines.append(f'<div class="item" style="border-left-color:{color};">')
        lines.append(f'<a class="item-title" href="{link}" target="_blank" rel="noopener">{title}</a>')
        lines.append(f'<div class="item-source">{feed_name}</div>')
        if summary:
            lines.append(f'<div class="item-summary">{escape(summary)}</div>')
        lines.append('</div>')

    lines.append('</div>')

    if cat in overflow:
        n = overflow[cat]
        lines.append(f'<div class="overflow-note">+{n} more items not shown (capped at 25 per category)</div>')

    lines.append('</section>')

# Footer
lines.append(f'''<footer class="footer">
  {stats["total_feeds"]} feeds checked &bull; {stats["feeds_errored"]} unreachable &bull; generated {DATE}
</footer>
</div>
</body>
</html>''')

html = "\n".join(lines)
out_path = f"/home/user/newsfeed/{DATE}.html"
Path(out_path).write_text(html, encoding="utf-8")
print(f"Written {len(html):,} bytes to {out_path}")
print(f"Items: {total_items}, Categories: {len(categories)}")
