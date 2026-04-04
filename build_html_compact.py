import json
from pathlib import Path

data = json.loads(Path("/home/user/newsfeed/2026-04-04.json").read_text())
stats = data["stats"]
overflow = data["overflow"]
categories = data["categories"]

total_feeds = stats["total_feeds"]
feeds_errored = stats["feeds_errored"]
num_cats = stats["categories_with_items"]
shown_count = sum(len(v) for v in categories.values())

summaries = {
  "The Four Psychological Disruptions of AI at Work": "Most AI-at-work discussions focus on jobs and economics, but this piece takes a rare look at the inner psychological experience of workers navigating AI — essential reading for leaders wanting to understand what employees are actually going through.",
  "The April Issue Is Here": "The Journal of Democracy's April issue tackles whether AI truly empowers autocrats, why democratic backsliding shouldn't have surprised us, and what we get wrong about populism — a must-read for anyone tracking global democracy's health.",
  "Daily Reading List – April 3, 2026 (#756)": "A curated set of links covering agent orchestration, a provocative take on Backstage being dead, and a critical look at how AI coding tools create hidden dependency problems.",
  "Adobe ColdFusion 2025 Bug: getBaseTagData() Doesn't Work Inside Closure": "If you're using ColdFusion 2025, this documented bug could silently break your custom tag logic inside closures — worth knowing before it bites you in production.",
  "9 Best Microsoft Planner Alternatives in 2026 (Free & Paid)": "If Microsoft Planner's limitations are holding your team back, this roundup covers the best alternatives available in 2026, both free and paid.",
  "OPAW: Optimal Bounds for Open Addressing Without Reordering": "A landmark CS paper claims to dramatically improve hash map performance — this post gives an honest assessment of whether it actually changes anything in practice.",
  "Absurd In Production": "After five months running a Postgres-only durable execution system in production, the author reports back on whether the bold 'no extra services needed' design held up — spoiler: it did.",
  "13 Best Paymo Alternatives for Freelancers & Agencies in 2026": "Paymo is solid for combining task management and invoicing, but if it doesn't fit your workflow, this guide covers 13 alternatives for freelancers and agencies.",
  "waybar-worldclock - a simple world clock for Waybar": "A lightweight Linux Waybar utility that shows world clock times in a tooltip on hover — no browser, no extra apps, just clean timezone awareness in your taskbar.",
  "Twitter's Recommendation Algorithm": "A look inside how Twitter's algorithm selects tweets for your timeline, straight from the engineering team — essential for understanding algorithmic content curation.",
  "Twitter's Blobstore Hardware Lifecycle Monitoring and Reporting Service": "Managing hundreds of thousands of servers is a massive challenge — this post reveals how Twitter built a system to track hardware lifecycle at that scale.",
  "How we scaled Reads On the Twitter Users Database": "Twitter shares the techniques they used to keep read performance fast on one of the world's most-queried user databases under massive load.",
  "Kerberizing Hadoop Clusters at Twitter": "This details how Twitter rolled out Kerberos authentication across their Hadoop infrastructure without disrupting operations — useful for data platform security.",
  "The data platform cluster operator service for Hadoop cluster management": "Twitter's engineers explain how they automated Hadoop cluster operations to reduce risk and human error as infrastructure grew.",
  "Constraint Management for cluster operation safety and reliability at Twitter": "How Twitter uses constraint management to keep cluster operations safe and predictable as infrastructure scale grew.",
  "How Twitter uses rasdaemon for hardware reliability": "Twitter explains how rasdaemon helps them monitor hardware errors across millions of components before they cascade into failures.",
  "Measuring the impact of Twitter network latency with CausalImpact": "How do you prove that latency improvements move the needle on revenue? Twitter applied Google's CausalImpact package to answer that rigorously.",
  "Stability and scalability for search": "How Twitter powers real-time search across tweets, users, and DMs using Elasticsearch at massive scale — useful reference for search infrastructure design.",
  "Data Quality Automation at Twitter": "Twitter built a platform letting customers define and automate data quality rules themselves — a good blueprint for teams battling data reliability issues.",
  "The one where Oskar explains Example Mapping": "Oskar walks through Example Mapping, a technique for turning fuzzy requirements into concrete, testable examples before writing a line of code.",
  "Interactive Rubber Ducking with GenAI": "A self-described GenAI sceptic honestly explores whether AI can serve as a useful thinking partner — the tension makes for a genuinely balanced take.",
  "The End of Coding? Wrong Question": "LLMs revealed how many developers don't enjoy coding — Oskar argues we've been asking the wrong question about what AI means for the profession.",
  "Parse, Don't Guess": "A practical lesson in why proper parsing beats defensive guessing, following up on a previous confession about transaction-handling trickery.",
  "How I cheated on transactions. Or how to make tradeoffs based on my Cloudflare D1 support": "We're told software design is about tradeoffs, but rarely taught how to make them — Oskar gets candid about a real compromise with Cloudflare D1.",
  "On rebuilding read models, Dead-Letter Queues and Why Letting Go is Sometimes the Answer": "Reader questions led Oskar into dead-letter queues and the counterintuitive wisdom of knowing when to simply discard a message rather than retry forever.",
  "Rebuilding Event-Driven Read Models in a safe and resilient way": "One of the trickier challenges in event-driven systems — this post covers events, projections, and practical patterns for safe, resilient read model rebuilding.",
  "Multi-tenancy and dynamic messaging workload distribution": "Multi-tenant messaging systems introduce complex workload distribution challenges — Oskar documents his findings on keeping things fair across tenants.",
  "Checkpointing the message processing": "A practical deep dive into checkpointing strategies for reliable message processing, with an unexpected SQL angle.",
  "Powering Multimodal Intelligence for Video Search": "Netflix is using multimodal AI to help filmmakers find exact moments across thousands of hours of raw footage — AI transforming real creative production workflows.",
  "docs.rs: building fewer targets by default": "Starting May 2026, docs.rs stops building multi-target docs by default — Rust crate maintainers need to act now to preserve cross-platform doc builds.",
  "Scaling Trust: How Salesforce's Security Team Uses Agentforce to Triage Security Reports at Speed": "Salesforce's security team built an AI-driven triage system using Agentforce to handle customer vulnerability reports at scale — agentic AI delivering real security value.",
  "How Amdahl's Law still applies to modern-day AI inefficiencies": "A 1967 CS law about parallelism turns out to be a sharp lens for diagnosing why enterprise AI productivity gains often disappoint.",
  "5 guidelines for effective brand measurement: Lessons from a survey scientist": "SurveyMonkey's survey scientists distill brand measurement into five actionable guidelines for more rigorous, reliable brand tracking insights.",
  "Our Transition to React Native": "Khan Academy shares the lessons and tradeoffs from moving their mobile app to React Native — a useful reference for teams considering cross-platform mobile.",
  "How Khan Academy Successfully Handled 2.5x Traffic in a Week": "Sudden 2.5x traffic spikes would break most systems — Khan Academy explains how their infrastructure absorbed the surge without going down.",
  "Go + Services = One Goliath Project": "Khan Academy's experience with Go microservices reveals the power and complexity of a statically typed language for large-scale service architecture.",
  "How to upgrade hundreds of React components without breaking production": "Upgrading React at scale is a minefield — Khan Academy's team shares the strategy that let them modernize hundreds of components safely.",
  "How Engineering Principles Can Help You Scale": "As teams grow, informal norms break down — Khan Academy shares the principles that helped them maintain quality and velocity without bureaucratic overhead.",
  "Making Websites Work with Windows High Contrast Mode": "Windows High Contrast Mode is a critical accessibility feature many sites break — Khan Academy shares what they learned about building sites that work for high contrast users.",
  "Kotlin for Python developers": "This guide bridges the gap by mapping familiar Python concepts to Kotlin equivalents — a fast on-ramp to the JVM if you're comfortable in Python.",
  "Using static analysis in Python, JavaScript and more to make your system safer": "Khan Academy shares practical lessons from applying static analysis across multiple languages to catch bugs before they reach production.",
  "Kotlin on the server at Khan Academy": "Khan Academy's bet on Kotlin for backend services — what drove the decision, how adoption went, and what they'd do differently.",
  "The Original Serverless Architecture is Still Here": "Before AWS Lambda, there was another 'serverless' — Khan Academy revisits the original model and makes a case for why it's still worth considering.",
  "What do software architects at Khan Academy do?": "The architect role is hard to define — Khan Academy offers a transparent look at what their architects actually own and influence day-to-day.",
  "New data pipeline management platform at Khan Academy": "Khan Academy walks through the platform they built to bring visibility and reliability to their data pipeline infrastructure.",
  "Untangling our Python Code": "Khan Academy shares techniques for bringing structure back to a sprawling, tangled Python codebase.",
  "Slicker: A Tool for Moving Things in Python": "Khan Academy built and open-sourced Slicker, a tool for safely moving Python modules and symbols during large-scale refactors.",
  "The Great Python Refactor of 2017 And Also 2018": "A multi-year, large-scale Python refactor — Khan Academy shares how they navigated it, what worked, and what they'd do differently.",
  "Working Remotely": "Khan Academy's hard-won lessons on making remote engineering work actually work — from a team distributed before it was common.",
  "Tips for giving your first code reviews": "Concrete, empathetic advice for developers doing their first code reviews without demoralizing their teammates.",
  "Let's Reduce! A Gentle Introduction to Javascript's Reduce Method": "Array.reduce is one of JavaScript's most powerful yet misunderstood methods — this gentle introduction finally makes it click.",
  "Creating Query Components with Apollo": "Khan Academy walks through building Apollo query components in a way that keeps React components readable and GraphQL fetching clean.",
  "Migrating to a Mobile Monorepo for React Native": "Khan Academy shares what drove them to a mobile monorepo, how the migration went, and whether the bet paid off.",
}

cat_colors = {
    "Leadership": "#e74c3c",
    "Politics": "#8e44ad",
    "Daily": "#2980b9",
    "Engineering": "#27ae60",
    "Engineering Blogs": "#e67e22",
}

def cid(name): return name.lower().replace(" ", "-")
def esc(s): return (s.replace("&","&amp;").replace("<","&lt;")
                    .replace(">","&gt;").replace('"',"&quot;"))

toc = "".join(
    f'<a class="pill" href="#{cid(c)}" style="background:{cat_colors.get(c,"#555")}">'
    f'{esc(c)} <small>({len(categories[c])}{"+" if c in overflow else ""})</small></a>'
    for c in categories
)

def render_section(cat):
    color = cat_colors.get(cat, "#555")
    items = categories[cat]
    rows = []
    for item in items:
        t = item["title"]; link = item["link"]; feed = item["feed_name"]
        pub = (item.get("published") or "")[:10]
        s = summaries.get(t, "")
        rows.append(
            f'<div class="item">'
            f'<div><a class="ititle" href="{esc(link)}">{esc(t)}</a></div>'
            f'<div class="meta">{esc(feed)}{(" · " + pub) if pub else ""}</div>'
            f'<div class="summary">{esc(s)}</div>'
            f'</div>'
        )
    extra = f'<p class="more">+{overflow[cat]} more items not shown</p>' if cat in overflow else ""
    return (
        f'<section id="{cid(cat)}" class="card" style="border-left:4px solid {color}">'
        f'<div class="cat-head"><h2 style="color:{color}">{esc(cat)}</h2>'
        f'<span class="cat-count">{len(items)} articles shown</span></div>'
        f'{"".join(rows)}{extra}'
        f'</section>'
    )

sections = "".join(render_section(c) for c in categories)
gen = data["generated_at"][:16].replace("T"," ")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Feed Digest: 2026-04-04</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f0f2f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#333}}
.wrap{{max-width:720px;margin:0 auto;padding:20px 16px}}
header{{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);color:#fff;padding:36px 20px;text-align:center}}
header p.label{{margin:0 0 6px;font-size:12px;letter-spacing:2px;text-transform:uppercase;opacity:.7}}
header h1{{margin:0 0 16px;font-size:30px;font-weight:700}}
.stats{{display:flex;justify-content:center;gap:24px;flex-wrap:wrap;font-size:14px;opacity:.85}}
.stats span strong{{font-size:22px;display:block}}
.toc{{background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.08);padding:14px 16px;margin-bottom:24px}}
.toc p{{margin:0 0 8px;font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#999;font-weight:600}}
.pill{{display:inline-block;margin:3px;padding:5px 12px;color:#fff;border-radius:20px;text-decoration:none;font-size:13px;font-weight:500}}
.pill small{{opacity:.85;font-size:11px}}
.card{{background:#fff;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.08);margin-bottom:24px;overflow:hidden}}
.cat-head{{padding:16px 20px 4px}}
.cat-head h2{{margin:0;font-size:19px}}
.cat-count{{font-size:12px;color:#888}}
.item{{padding:12px 20px;border-bottom:1px solid #f0f0f0}}
.item:last-child{{border-bottom:none}}
.ititle{{font-weight:600;color:#1a1a2e;text-decoration:none;font-size:15px}}
.ititle:hover{{text-decoration:underline}}
.meta{{font-size:12px;color:#888;margin:3px 0 5px}}
.summary{{font-size:13px;color:#444;line-height:1.55}}
.more{{padding:8px 20px 16px;margin:0;font-size:13px;color:#888;font-style:italic}}
footer{{text-align:center;padding:20px 0 36px;font-size:13px;color:#999}}
@media(max-width:600px){{.wrap{{padding:12px 10px}}header{{padding:24px 14px}}}}
</style>
</head>
<body>
<header>
<p class="label">Daily Digest</p>
<h1>April 4, 2026</h1>
<div class="stats">
<span><strong>{shown_count}</strong>articles</span>
<span><strong>{total_feeds - feeds_errored}</strong>feeds checked</span>
<span><strong>{num_cats}</strong>categories</span>
</div>
</header>
<div class="wrap">
<nav class="toc"><p>Jump to category</p><div>{toc}</div></nav>
{sections}
<footer>
<p>{total_feeds} feeds checked &middot; {feeds_errored} unreachable</p>
<p>Generated {gen} UTC</p>
</footer>
</div>
</body>
</html>"""

Path("/home/user/newsfeed/2026-04-04.html").write_text(html)
print(f"Compact HTML: {len(html)} bytes, ~{len(html)//4} estimated tokens")
