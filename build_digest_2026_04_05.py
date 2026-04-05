#!/usr/bin/env python3
"""Build HTML digest for 2026-04-05 with hand-crafted summaries."""

import json

with open('/home/user/newsfeed/2026-04-05.json') as f:
    data = json.load(f)

stats = data['stats']
categories = data['categories']
overflow = data.get('overflow', {})

# --- Summaries keyed by (category, index) ---
SUMMARIES = {
    # Business
    ('Business', 0): (
        "A practical framework for evaluating startup pitches through five key diagnostic "
        "questions—useful for investors, advisors, or founders who want to stress-test an "
        "idea quickly after hearing it."
    ),

    # Engineering
    ('Engineering', 0): (
        "Goes well beyond the basics: this curl guide covers API testing, authentication, "
        "SSL inspection, and timing analysis with real sysadmin one-liners you can steal "
        "immediately."
    ),
    ('Engineering', 1): (
        "Microsoft has quietly expanded its AI lineup with three new first-party MAI models "
        "on Foundry—covering transcription, voice generation, and image creation—worth "
        "evaluating if you're shopping for alternatives to OpenAI or Google."
    ),
    ('Engineering', 2): (
        "A free PDF scan of a rare 1984 German printer guide featuring a fully commented "
        "disassembly—a fascinating historical artifact for retrocomputing enthusiasts or "
        "anyone curious about how printers worked at the hardware level."
    ),
    ('Engineering', 3): (
        "A thorough xargs tutorial covering parallel execution, safe filename handling, bulk "
        "file operations, and multi-server SSH commands—essential reading for leveling up "
        "your shell scripting game."
    ),
    ('Engineering', 4): (
        "Reproducible bug report showing that Adobe ColdFusion 2025 silently breaks "
        "getBaseTagData() inside closures—worth knowing immediately if your code uses that "
        "pattern."
    ),
    ('Engineering', 5): (
        "Twitter's official breakdown of how its timeline ranking algorithm selects tweets, "
        "offering a rare transparent look at one of the world's most influential "
        "content-ranking systems."
    ),
    ('Engineering', 6): (
        "How Twitter monitors hardware lifecycle across hundreds of thousands of servers and "
        "millions of components—a detailed reference for large-scale infrastructure teams "
        "managing bare-metal fleets."
    ),
    ('Engineering', 7): (
        "Twitter shares the techniques used to scale read throughput on its massive users "
        "database, with lessons directly applicable to any team hitting read bottlenecks at "
        "scale."
    ),
    ('Engineering', 8): (
        "A technical walkthrough of adding Kerberos authentication to Hadoop clusters at "
        "Twitter's scale—useful for any team needing to harden Hadoop security without "
        "disrupting existing workloads."
    ),
    ('Engineering', 9): (
        "Twitter describes the operator service that automates Hadoop cluster management to "
        "minimize outage risk as data platform size grows—a solid reference architecture "
        "for large data teams."
    ),
    ('Engineering', 10): (
        "How Twitter uses constraint management to prevent dangerous cluster operations from "
        "causing cascading failures—a practical approach to encoding operational safety "
        "rules at scale."
    ),
    ('Engineering', 11): (
        "Twitter's use of rasdaemon to proactively catch hardware errors across its data "
        "center fleet before they cause outages—worth reading for anyone running bare-metal "
        "infrastructure at scale."
    ),
    ('Engineering', 12): (
        "Twitter applies Google's CausalImpact framework to quantify how network latency "
        "improvements affect engagement and revenue—a compelling case for using causal "
        "inference to justify infrastructure investments."
    ),
    ('Engineering', 13): (
        "An inside look at how Twitter powers real-time search across tweets, users, and "
        "DMs using Elasticsearch—useful reading for engineers building or scaling "
        "large-scale search systems."
    ),
    ('Engineering', 14): (
        "How Twitter built an automated data quality platform that lets teams define and "
        "run data checks at pipeline scale—a valuable reference for anyone wrestling with "
        "data reliability."
    ),
    ('Engineering', 15): (
        "Oskar Dudycz explains Example Mapping, a structured workshop technique for "
        "surfacing concrete examples that clarify requirements before coding starts—great "
        "for teams that frequently discover misunderstandings mid-sprint."
    ),
    ('Engineering', 16): (
        "A skeptical-but-practical look at using GenAI as an interactive rubber duck: "
        "Oskar Dudycz—a self-described AI skeptic—shares when this actually helps and "
        "where it falls short."
    ),
    ('Engineering', 17): (
        "Oskar argues that LLMs haven't killed coding—they've just revealed how many "
        "developers never liked it in the first place—a thought-provoking counterpoint to "
        "the 'AI ends programming' narrative."
    ),
    ('Engineering', 18): (
        "A concise post on using strict parsing instead of guessing at data shapes to "
        "eliminate a whole class of subtle production bugs—good foundational advice backed "
        "by a real-world example."
    ),
    ('Engineering', 19): (
        "An honest account of making pragmatic transaction trade-offs when building on "
        "Cloudflare D1's edge database—valuable for anyone navigating the constraints of "
        "serverless or edge data stores."
    ),
    ('Engineering', 20): (
        "Explores when Dead-Letter Queues are the right answer and when it's better to "
        "simply let a message go—important nuance for teams building resilient "
        "event-driven systems."
    ),
    ('Engineering', 21): (
        "A detailed guide to safely rebuilding read models in event-driven architectures "
        "without data loss or downtime, covering inline vs. async projections—essential "
        "for teams using event sourcing."
    ),
    ('Engineering', 22): (
        "Covers patterns for distributing messaging workloads fairly across tenants in "
        "multi-tenant SaaS systems—useful for anyone facing noisy-neighbor problems in "
        "their message processing pipeline."
    ),
    ('Engineering', 23): (
        "Dives into checkpointing strategies to achieve reliable at-least-once or "
        "exactly-once message processing semantics—practical guidance for teams building "
        "event-driven data pipelines."
    ),
    ('Engineering', 24): (
        "Introduces and distinguishes the core roles—consumers, projectors, and "
        "reactors—in the Emmett event-driven framework, clarifying an often-muddled "
        "part of event sourcing design."
    ),

    # Engineering Blogs (KA Engineering — no excerpts available)
    ('Engineering Blogs', 0): (
        "Khan Academy's account of migrating their mobile apps to React Native, sharing "
        "hard-won lessons from moving a large production codebase."
    ),
    ('Engineering Blogs', 1): (
        "How Khan Academy's engineering team scaled to handle a sudden 2.5x traffic surge "
        "in a single week—a real-world case study in rapid, high-stakes scaling."
    ),
    ('Engineering Blogs', 2): (
        "Khan Academy's experience adopting Go for backend services, examining the "
        "trade-offs encountered when migrating a large-scale production system to a new "
        "language."
    ),
    ('Engineering Blogs', 3): (
        "Khan Academy's strategy for safely upgrading hundreds of React components in "
        "production—essential reading for teams facing large-scale frontend refactors "
        "they can't afford to break."
    ),
    ('Engineering Blogs', 4): (
        "How codified engineering principles guided Khan Academy's scaling decisions as the "
        "organization grew—useful framing for engineering leaders trying to build "
        "consistent team culture."
    ),
    ('Engineering Blogs', 5): (
        "Practical CSS techniques for making websites work correctly under Windows High "
        "Contrast Mode, drawn from Khan Academy's accessibility work—a must-read for "
        "frontend engineers caring about inclusive design."
    ),
    ('Engineering Blogs', 6): (
        "A targeted guide bridging Python and Kotlin idioms to help Python developers get "
        "productive in Kotlin quickly—handy if your team is considering a Kotlin "
        "migration."
    ),
    ('Engineering Blogs', 7): (
        "Khan Academy's approach to deploying static analysis across Python, JavaScript, "
        "and other languages to catch bugs early—practical advice for teams wanting "
        "better code quality without slowing delivery."
    ),
    ('Engineering Blogs', 8): (
        "Production learnings from running Kotlin on the server side at Khan Academy, "
        "covering performance characteristics, tooling choices, and team adoption "
        "challenges."
    ),
    ('Engineering Blogs', 9): (
        "An argument that the original serverless model still has real merit today—a "
        "thought-provoking historical perspective for cloud architects reconsidering "
        "architecture choices."
    ),
    ('Engineering Blogs', 10): (
        "A candid look at what software architects actually do day-to-day at Khan Academy, "
        "clarifying the role for engineers curious about engineering leadership "
        "structures."
    ),
    ('Engineering Blogs', 11): (
        "Khan Academy introduces its new internal data pipeline management platform, "
        "detailing the problems it solves and the design decisions behind it."
    ),
    ('Engineering Blogs', 12): (
        "How Khan Academy attacked a tangled Python codebase to reduce coupling and improve "
        "maintainability—useful for anyone managing a large, aging Python project."
    ),
    ('Engineering Blogs', 13): (
        "Khan Academy open-sources Slicker, a tool for safely moving code and symbols "
        "across Python files—a practical utility that makes large refactoring efforts "
        "much less painful."
    ),
    ('Engineering Blogs', 14): (
        "Khan Academy's multi-year Python refactoring story, sharing what worked, what "
        "didn't, and how to sustain a large refactor over an extended timeframe."
    ),
    ('Engineering Blogs', 15): (
        "Khan Academy's engineering team shares practices and lessons from embracing "
        "distributed remote work—relevant for any team navigating the shift to async "
        "collaboration."
    ),
    ('Engineering Blogs', 16): (
        "Practical, empathetic advice for engineers giving code reviews for the first "
        "time—a helpful read for junior developers or anyone new to a team's review "
        "culture."
    ),
    ('Engineering Blogs', 17): (
        "A gentle, beginner-friendly walkthrough of JavaScript's Array.reduce that "
        "demystifies one of the most powerful but most frequently misunderstood "
        "functional programming methods."
    ),
    ('Engineering Blogs', 18): (
        "Khan Academy demonstrates patterns for building reusable Apollo GraphQL query "
        "components in React—worth reading if you're trying to clean up repetitive "
        "data-fetching code."
    ),
    ('Engineering Blogs', 19): (
        "Khan Academy's journey migrating React Native code to a monorepo structure, "
        "sharing tooling choices, trade-offs, and lessons that could save you significant "
        "pain."
    ),
    ('Engineering Blogs', 20): (
        "How Khan Academy uses Memcached at scale to power its content delivery "
        "infrastructure—a concrete case study in high-performance caching architecture."
    ),
    ('Engineering Blogs', 21): (
        "Khan Academy profiles Memcached performance on App Engine, sharing techniques and "
        "findings relevant to any team chasing cache efficiency on managed infrastructure."
    ),
    ('Engineering Blogs', 22): (
        "Khan Academy benchmarks multiple programming languages on App Engine Flex, giving "
        "teams data-driven guidance for language choices in performance-sensitive "
        "services."
    ),
    ('Engineering Blogs', 23): (
        "A roundup of Khan Academy's recent open-source releases and contributions—worth "
        "a look if you're following edtech engineering or want to discover useful OSS "
        "tools."
    ),
    ('Engineering Blogs', 24): (
        "How Khan Academy automated the tedious process of generating App Store "
        "screenshots, freeing up engineering time and eliminating a painful manual "
        "workflow."
    ),
}

# --- Category colors ---
CAT_COLORS = {
    'Business': '#e74c3c',
    'Engineering': '#3498db',
    'Engineering Blogs': '#2ecc71',
}
DEFAULT_COLORS = ['#9b59b6', '#f39c12', '#1abc9c', '#e67e22', '#e91e63']

def get_cat_color(cat, idx):
    if cat in CAT_COLORS:
        return CAT_COLORS[cat]
    return DEFAULT_COLORS[idx % len(DEFAULT_COLORS)]

total_items = sum(len(items) for items in categories.values())
cat_names = list(categories.keys())

# Build category sections
sections_html = ''
toc_items = ''

for cat_idx, (cat, items) in enumerate(categories.items()):
    color = get_cat_color(cat, cat_idx)
    cat_id = cat.lower().replace(' ', '-')
    toc_items += f'<a href="#{cat_id}" class="toc-pill" style="background:{color}20;color:{color};border:1.5px solid {color}40">{cat} <span class="toc-count">{len(items)}</span></a>\n'

    items_html = ''
    for i, item in enumerate(items):
        summary = SUMMARIES.get((cat, i), '')
        title = item['title']
        link = item.get('link', '#')
        feed_name = item.get('feed_name', '')
        items_html += f'''
        <div class="item">
          <div class="item-title"><a href="{link}" target="_blank" rel="noopener">{title}</a></div>
          <div class="item-feed">{feed_name}</div>
          <div class="item-summary">{summary}</div>
        </div>'''

    ov = overflow.get(cat, 0)
    overflow_note = ''
    if ov:
        overflow_note = f'<div class="overflow-note">+{ov} more items not shown</div>'

    sections_html += f'''
    <section class="cat-card" id="{cat_id}" style="border-left:4px solid {color}">
      <h2 class="cat-title" style="color:{color}">{cat}</h2>
      {items_html}
      {overflow_note}
    </section>'''

# Footer stats
feeds_checked = stats['total_feeds']
feeds_errored = stats['feeds_errored']
feeds_ok = stats['feeds_fetched']

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feed Digest: 2026-04-05</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif;
    background: #f0f2f5;
    color: #333;
    line-height: 1.6;
  }}
  a {{ color: inherit; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}

  .wrapper {{
    max-width: 720px;
    margin: 0 auto;
    padding: 0 16px 48px;
  }}

  /* Header */
  .header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
    padding: 40px 24px 32px;
    margin-bottom: 24px;
  }}
  .header-inner {{
    max-width: 720px;
    margin: 0 auto;
  }}
  .header h1 {{
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
  }}
  .header-date {{
    font-size: 0.95rem;
    opacity: 0.75;
    margin-bottom: 20px;
  }}
  .header-stats {{
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
  }}
  .stat {{
    text-align: center;
  }}
  .stat-num {{
    font-size: 1.6rem;
    font-weight: 700;
    display: block;
    line-height: 1.1;
  }}
  .stat-label {{
    font-size: 0.75rem;
    opacity: 0.65;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  /* TOC */
  .toc {{
    background: #fff;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
  }}
  .toc h3 {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #888;
    margin-bottom: 12px;
  }}
  .toc-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .toc-pill {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    transition: opacity 0.15s;
  }}
  .toc-pill:hover {{ opacity: 0.8; text-decoration: none; }}
  .toc-count {{
    background: rgba(0,0,0,0.12);
    border-radius: 10px;
    padding: 1px 6px;
    font-size: 0.75rem;
    font-weight: 600;
  }}

  /* Category cards */
  .cat-card {{
    background: #fff;
    border-radius: 10px;
    padding: 24px 24px 16px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
  }}
  .cat-title {{
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  /* Items */
  .item {{
    padding: 14px 0;
    border-bottom: 1px solid #f0f2f5;
  }}
  .item:last-of-type {{
    border-bottom: none;
  }}
  .item-title {{
    font-weight: 600;
    font-size: 0.97rem;
    margin-bottom: 3px;
    line-height: 1.4;
  }}
  .item-title a {{
    color: #1a1a2e;
  }}
  .item-title a:hover {{
    color: #0f3460;
    text-decoration: underline;
  }}
  .item-feed {{
    font-size: 0.78rem;
    color: #aaa;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}
  .item-summary {{
    font-size: 0.875rem;
    color: #555;
    line-height: 1.55;
  }}

  /* Overflow note */
  .overflow-note {{
    margin-top: 14px;
    padding: 10px 14px;
    background: #f8f9fa;
    border-radius: 6px;
    font-size: 0.82rem;
    color: #888;
    text-align: center;
    font-style: italic;
  }}

  /* Footer */
  .footer {{
    max-width: 720px;
    margin: 0 auto;
    padding: 0 16px 32px;
    font-size: 0.8rem;
    color: #aaa;
    text-align: center;
    line-height: 1.7;
  }}
  .footer strong {{ color: #888; }}
</style>
</head>
<body>

<div class="header">
  <div class="header-inner">
    <h1>Feed Digest</h1>
    <div class="header-date">Sunday, April 5, 2026 &mdash; Last 24 hours</div>
    <div class="header-stats">
      <div class="stat">
        <span class="stat-num">{total_items}</span>
        <span class="stat-label">Items</span>
      </div>
      <div class="stat">
        <span class="stat-num">{feeds_ok}</span>
        <span class="stat-label">Feeds</span>
      </div>
      <div class="stat">
        <span class="stat-num">{len(cat_names)}</span>
        <span class="stat-label">Categories</span>
      </div>
    </div>
  </div>
</div>

<div class="wrapper">

  <nav class="toc">
    <h3>Categories</h3>
    <div class="toc-pills">
      {toc_items}
    </div>
  </nav>

  {sections_html}

</div>

<footer class="footer">
  <strong>{feeds_checked}</strong> feeds checked &bull; <strong>{feeds_ok}</strong> reachable &bull; <strong>{feeds_errored}</strong> unreachable
</footer>

</body>
</html>'''

output_path = '/home/user/newsfeed/digest_2026-04-05.html'
with open(output_path, 'w') as f:
    f.write(html)

print(f"Written: {output_path}")
print(f"Total items summarized: {total_items}")
print(f"Categories: {len(cat_names)} ({', '.join(cat_names)})")
