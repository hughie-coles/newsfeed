import json
from pathlib import Path

data = json.loads(Path("/home/user/newsfeed/2026-04-04.json").read_text())

stats = data["stats"]
overflow = data["overflow"]
errors = data["errors"]
categories = data["categories"]

total_feeds = stats["total_feeds"]
feeds_errored = stats["feeds_errored"]
total_items = stats["total_items"]
num_cats = stats["categories_with_items"]

# All items shown (after cap)
shown_count = sum(len(v) for v in categories.values())

# Summaries keyed by title
summaries = {
  "The Four Psychological Disruptions of AI at Work": "Most AI-at-work discussions focus on jobs and economics, but this piece takes a rare look at the inner psychological experience of workers navigating AI — making it essential reading for leaders who want to understand what employees are actually going through.",
  "The April Issue Is Here": "The Journal of Democracy's April issue tackles whether AI truly empowers autocrats, why democratic backsliding shouldn't have surprised us, and what we keep getting wrong about populism — a must-read for anyone tracking the health of global democracy.",
  "Daily Reading List – April 3, 2026 (#756)": "A curated set of links covering agent orchestration, a provocative take on Backstage being dead, and a critical look at how AI coding tools are creating hidden dependency problems.",
  "Adobe ColdFusion 2025 Bug: getBaseTagData() Doesn't Work Inside Closure": "If you're using ColdFusion 2025, this documented bug could silently break your custom tag logic inside closures — worth checking before it causes you a headache.",
  "9 Best Microsoft Planner Alternatives in 2026 (Free & Paid)": "If Microsoft Planner's limitations are holding your team back, this roundup covers the best alternatives available in 2026, with both free and paid options evaluated.",
  "OPAW: Optimal Bounds for Open Addressing Without Reordering": "A landmark computer science paper claims to dramatically improve hash map performance — but does it actually change anything in practice? This post cuts through the hype with an honest assessment.",
  "Absurd In Production": "After five months running a Postgres-only durable execution system in production, the author reports back on whether the bold 'no extra services needed' design actually held up — spoiler: it did.",
  "13 Best Paymo Alternatives for Freelancers & Agencies in 2026": "Paymo is solid for combining task management and invoicing, but if it's not quite fitting your workflow, this guide breaks down 13 alternatives tailored for freelancers and agencies in 2026.",
  "waybar-worldclock - a simple world clock for Waybar": "A lightweight utility for Linux Waybar users that surfaces world clock times in a tooltip on hover — no browser needed, no extra apps, just clean timezone awareness in your taskbar.",
  "Twitter's Recommendation Algorithm": "A rare look inside how Twitter's algorithm decides which tweets land on your timeline, straight from the engineering team — essential context for anyone trying to understand algorithmic content curation.",
  "Twitter's Blobstore Hardware Lifecycle Monitoring and Reporting Service": "Managing hundreds of thousands of servers is a staggering operational challenge — this post reveals how Twitter built a system to track the full lifecycle of hardware at that scale.",
  "How we scaled Reads On the Twitter Users Database": "Scaling read performance on one of the world's most-queried user databases is no small feat — Twitter's engineers share the techniques they used to keep it fast under massive load.",
  "Kerberizing Hadoop Clusters at Twitter": "Securing large-scale Hadoop clusters is notoriously complex — this post details how Twitter rolled out Kerberos authentication across their infrastructure without disrupting operations.",
  "The data platform cluster operator service for Hadoop cluster management": "As data infrastructure grows, manual cluster management becomes untenable — Twitter's engineers explain how they automated Hadoop cluster operations to reduce risk and human error.",
  "Constraint Management for cluster operation safety and reliability at Twitter": "Outages and data loss risk grow with infrastructure scale — this post reveals how Twitter uses constraint management to keep cluster operations safe and predictable.",
  "How Twitter uses rasdaemon for hardware reliability": "With millions of hardware components in play, catching failures before they cascade is critical — Twitter explains how rasdaemon helps them monitor and maintain hardware reliability at scale.",
  "Measuring the impact of Twitter network latency with CausalImpact": "How do you prove that reducing network latency actually moves the needle on revenue and engagement? Twitter applied Google's CausalImpact package to answer that question rigorously.",
  "Stability and scalability for search": "Powering real-time search across tweets, users, and DMs at Twitter's scale is a serious engineering challenge — this post dives into how Elasticsearch is tuned to handle it.",
  "Data Quality Automation at Twitter": "Manual data quality checks don't scale — Twitter built a platform that lets customers define and automate their own data quality rules, and this post explains how they did it.",
  "The one where Oskar explains Example Mapping": "Using a 'Friends'-style framing, Oskar walks through Example Mapping, a collaborative technique for turning fuzzy requirements into concrete, testable examples before you write a single line of code.",
  "Interactive Rubber Ducking with GenAI": "A self-described GenAI sceptic explores whether AI can actually serve as a useful thinking partner — the tension between skepticism and practical utility makes for a genuinely honest take.",
  "The End of Coding? Wrong Question": "The rise of LLMs has exposed something surprising: many developers don't actually enjoy coding — and Oskar argues we've been asking the wrong question about what AI means for the profession.",
  "Parse, Don't Guess": "Following up on a previous confession about transaction handling trickery, Oskar shares the clean fix — a practical lesson in why proper parsing beats defensive guessing every time.",
  "How I cheated on transactions. Or how to make tradeoffs based on my Cloudflare D1 support": "We're told software design is all about tradeoffs, but rarely taught how to actually make them — Oskar gets candid about a pragmatic compromise he made with Cloudflare D1 transaction support.",
  "On rebuilding read models, Dead-Letter Queues and Why Letting Go is Sometimes the Answer": "After writing about resilient read model rebuilding, reader questions led Oskar deeper into dead-letter queues and the counterintuitive wisdom of knowing when to simply discard a message.",
  "Rebuilding Event-Driven Read Models in a safe and resilient way": "Rebuilding read models without causing chaos is one of the trickier challenges in event-driven systems — this post blends events, projections, and practical patterns into a coherent recipe.",
  "Multi-tenancy and dynamic messaging workload distribution": "Multi-tenant messaging systems introduce complex workload distribution challenges — Oskar documents his findings on keeping things fair and dynamic across tenants.",
  "Checkpointing the message processing": "An unexpected pairing of Super Frog and SQL if-statements sets up a practical deep dive into checkpointing strategies for reliable message processing.",
  "Powering Multimodal Intelligence for Video Search": "Netflix is using multimodal AI to help filmmakers find the exact moments they need across thousands of hours of raw footage — a fascinating look at how AI is transforming creative production workflows.",
  "docs.rs: building fewer targets by default": "Starting May 2026, docs.rs will stop building multi-target documentation by default — Rust crate maintainers need to act now if they want to preserve cross-platform doc builds.",
  "Scaling Trust: How Salesforce's Security Team Uses Agentforce to Triage Security Reports at Speed": "Salesforce's security operations team built an AI-driven triage system using Agentforce to handle customer-reported vulnerabilities at scale — a concrete example of agentic AI delivering real security value.",
  "How Amdahl's Law still applies to modern-day AI inefficiencies": "A 1967 computer science law about parallelism turns out to be a surprisingly sharp lens for diagnosing why AI-driven productivity gains often disappoint at the enterprise level.",
  "5 guidelines for effective brand measurement: Lessons from a survey scientist": "SurveyMonkey's survey science team distills brand measurement into five actionable guidelines — useful for marketers who want more rigorous, reliable insights from their brand tracking efforts.",
  "Our Transition to React Native": "Khan Academy's engineering team shares the lessons and tradeoffs from moving their mobile app to React Native — a useful reference for any team considering a similar cross-platform shift.",
  "How Khan Academy Successfully Handled 2.5x Traffic in a Week": "Sudden 2.5x traffic spikes would break most systems — Khan Academy's engineers explain how their infrastructure absorbed the surge without going down.",
  "Go + Services = One Goliath Project": "Khan Academy's experience combining Go and microservices reveals both the power and the complexity that comes with betting on a statically typed language for a large-scale service architecture.",
  "How to upgrade hundreds of React components without breaking production": "Upgrading React at scale is a minefield of subtle breakages — Khan Academy's team shares the strategy that let them modernize hundreds of components safely.",
  "How Engineering Principles Can Help You Scale": "As engineering teams grow, informal norms break down — Khan Academy shares the principles that helped them maintain quality and velocity without adding bureaucratic overhead.",
  "Making Websites Work with Windows High Contrast Mode": "Windows High Contrast Mode is a critical accessibility feature that many sites quietly break — Khan Academy's engineers share what they learned about building sites that actually work for high contrast users.",
  "Kotlin for Python developers": "If you're comfortable in Python and curious about Kotlin, this guide bridges the gap by mapping familiar Python concepts to their Kotlin equivalents — a fast on-ramp to a powerful JVM language.",
  "Using static analysis in Python, JavaScript and more to make your system safer": "Static analysis catches bugs before they reach production — Khan Academy's engineers share practical lessons from applying it across multiple languages in a real-world codebase.",
  "Kotlin on the server at Khan Academy": "Khan Academy made a bet on Kotlin for backend services — this post covers what drove the decision, how adoption went, and what they'd do differently.",
  "The Original Serverless Architecture is Still Here": "Before AWS Lambda, there was another kind of 'serverless' — Khan Academy revisits the original model and makes a case for why it's still worth considering today.",
  "What do software architects at Khan Academy do?": "The architect role is notoriously hard to define — Khan Academy offers a transparent look at what their architects actually own, decide, and influence day-to-day.",
  "New data pipeline management platform at Khan Academy": "Managing complex data pipelines at scale demands real tooling — Khan Academy walks through the platform they built to bring visibility and reliability to their data infrastructure.",
  "Untangling our Python Code": "Large Python codebases accumulate messy dependencies over time — Khan Academy shares the techniques they used to bring structure and clarity back to a sprawling codebase.",
  "Slicker: A Tool for Moving Things in Python": "Refactoring Python at scale means moving code around safely and often — Khan Academy built and open-sourced Slicker, a tool designed to make that process far less painful.",
  "The Great Python Refactor of 2017 And Also 2018": "A multi-year, large-scale Python refactor is the kind of project that can derail a team — Khan Academy shares how they navigated it, what worked, and what they'd do differently.",
  "Working Remotely": "Khan Academy's team shares hard-won lessons on making remote work actually work — practical insights from a team that was distributed before it was common.",
  "Tips for giving your first code reviews": "Code review is a skill, not just a checklist — Khan Academy's engineers offer concrete, empathetic advice for developers doing their first reviews without demoralizing their teammates.",
  "Let's Reduce! A Gentle Introduction to Javascript's Reduce Method": "Array.reduce is one of JavaScript's most powerful yet most misunderstood methods — this gentle introduction breaks it down in a way that finally makes it click.",
  "Creating Query Components with Apollo": "Apollo's query components can clean up your GraphQL data fetching significantly — Khan Academy walks through how to build them in a way that keeps your React components readable and maintainable.",
  "Migrating to a Mobile Monorepo for React Native": "Moving mobile code into a monorepo is a major structural bet — Khan Academy shares what drove them to consolidate, how the migration went, and whether it paid off.",
}

# Category colors
cat_colors = {
    "Leadership": "#e74c3c",
    "Politics": "#8e44ad",
    "Daily": "#2980b9",
    "Engineering": "#27ae60",
    "Engineering Blogs": "#e67e22",
}

def cat_id(name):
    return name.lower().replace(" ", "-")

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# Build TOC pills
toc_items = []
for cat in categories:
    color = cat_colors.get(cat, "#555")
    count = len(categories[cat])
    if cat in overflow:
        count_label = f"{count}+"
    else:
        count_label = str(count)
    toc_items.append(
        f'<a href="#{cat_id(cat)}" style="display:inline-block;margin:4px;padding:6px 14px;background:{color};color:#fff;border-radius:20px;text-decoration:none;font-size:14px;font-weight:500;">'
        f'{esc(cat)} <span style="opacity:0.85;font-size:12px;">({count_label})</span></a>'
    )

# Build category sections
sections_html = []
for cat in categories:
    color = cat_colors.get(cat, "#555")
    items = categories[cat]
    items_html = []
    for item in items:
        title = item["title"]
        link = item["link"]
        feed = item["feed_name"]
        summary = summaries.get(title, "")
        pub = item.get("published") or ""
        pub_display = pub[:10] if pub else ""
        items_html.append(
            f'<div style="padding:14px 0;border-bottom:1px solid #f0f0f0;">'
            f'<div style="margin-bottom:4px;">'
            f'<a href="{esc(link)}" style="font-weight:600;color:#1a1a2e;text-decoration:none;font-size:15px;">{esc(title)}</a>'
            f'</div>'
            f'<div style="font-size:12px;color:#888;margin-bottom:6px;">'
            f'{esc(feed)}{(" &middot; " + pub_display) if pub_display else ""}'
            f'</div>'
            f'<div style="font-size:14px;color:#444;line-height:1.55;">{esc(summary)}</div>'
            f'</div>'
        )
    
    overflow_note = ""
    if cat in overflow:
        n = overflow[cat]
        overflow_note = (
            f'<p style="margin:12px 0 0;font-size:13px;color:#888;font-style:italic;">'
            f'+{n} more items not shown</p>'
        )
    
    sections_html.append(
        f'<section id="{cat_id(cat)}" style="background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.08);'
        f'margin-bottom:28px;padding:0;overflow:hidden;">'
        f'<div style="background:#fff;border-left:4px solid {color};padding:18px 22px 4px 22px;">'
        f'<h2 style="margin:0;font-size:20px;color:{color};">{esc(cat)}</h2>'
        f'<p style="margin:4px 0 0;font-size:13px;color:#888;">{len(items)} article{"s" if len(items)!=1 else ""} shown</p>'
        f'</div>'
        f'<div style="padding:0 22px 18px 22px;">'
        f'{"".join(items_html)}'
        f'{overflow_note}'
        f'</div>'
        f'</section>'
    )

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feed Digest: 2026-04-04</title>
<style>
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  padding: 0;
  background: #f0f2f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #333;
}}
a:hover {{ text-decoration: underline !important; }}
@media (max-width: 600px) {{
  .container {{ padding: 0 10px; }}
  header {{ padding: 28px 16px !important; }}
}}
</style>
</head>
<body>

<header style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#fff;padding:40px 20px;text-align:center;">
  <div style="max-width:720px;margin:0 auto;">
    <p style="margin:0 0 6px;font-size:13px;letter-spacing:2px;text-transform:uppercase;opacity:0.7;">Daily Digest</p>
    <h1 style="margin:0 0 16px;font-size:32px;font-weight:700;letter-spacing:-0.5px;">April 4, 2026</h1>
    <div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap;font-size:14px;opacity:0.85;">
      <span><strong style="font-size:22px;display:block;">{shown_count}</strong>articles</span>
      <span><strong style="font-size:22px;display:block;">{total_feeds - feeds_errored}</strong>feeds checked</span>
      <span><strong style="font-size:22px;display:block;">{num_cats}</strong>categories</span>
    </div>
  </div>
</header>

<div class="container" style="max-width:720px;margin:0 auto;padding:24px 16px;">

  <nav style="background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.08);padding:16px 18px;margin-bottom:28px;">
    <p style="margin:0 0 10px;font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#999;font-weight:600;">Jump to category</p>
    <div>{"".join(toc_items)}</div>
  </nav>

  {"".join(sections_html)}

  <footer style="text-align:center;padding:24px 0 40px;font-size:13px;color:#999;">
    <p style="margin:0 0 4px;">{total_feeds} feeds checked &middot; {feeds_errored} unreachable</p>
    <p style="margin:0;">Generated {data["generated_at"][:16].replace("T"," ")} UTC</p>
  </footer>

</div>
</body>
</html>"""

Path("/home/user/newsfeed/2026-04-04.html").write_text(html)
print(f"Written {len(html)} bytes")
