import json, html, re
from datetime import datetime, timezone

DATE = "2026-04-06"

with open(f"{DATE}.json") as f:
    data = json.load(f)

stats = data["stats"]
cats = data["categories"]
overflow = data.get("overflow", {})

# ── AI-generated summaries (title + excerpt → 1-2 sentences) ──────────────
SUMMARIES = {
    # Leadership
    "https://bradenkelley.com/2026/04/misunderstanding-big-ideas-is-very-dangerous/":
        "Greg Satell examines how dangerously misinterpreting major intellectual frameworks—like Fukuyama's \"End of History\"—leads organisations to make fatally flawed strategic decisions. The article warns that superficially adopting big ideas without true understanding can be more harmful than ignorance.",

    # Politics
    "https://www.journalofdemocracy.org/online-exclusive/why-viktor-orban-is-in-trouble/":
        "A series of unforced errors, poor governance results, and the emergence of a credible opposition are threatening Viktor Orbán's grip on Hungary. The piece extracts wider lessons about the conditions under which illiberal leaders can be successfully defeated.",

    # Agile
    "https://bobgalen.substack.com/p/lazy-strategy-lazy-hiring-lazy-leadership":
        "Bob Galen argues that the wave of mass tech layoffs at companies like Amazon, Meta, and Oracle reflects a failure of leadership strategy rather than genuine restructuring. He connects undisciplined headcount growth to lazy strategy and ultimately lazy leadership.",

    # Engineering
    "https://www.red-gate.com/simple-talk/development/syntax-and-data-structures-in-esproc-spl-a-complete-guide/":
        "A comprehensive guide to esProc SPL's core syntax and its table-based data structures, aimed at developers transitioning from Python. Covers SPL's primary data structure and common analytical operations.",

    "https://world.hey.com/dhh/panther-lake-is-the-real-deal-4bd731f1":
        "DHH reports impressive real-world numbers from Intel's Panther Lake chip in the Dell XPS 14—idle power as low as 1.4W and up to 47+ hours of theoretical battery life. He considers it a massive leap over the AMD-powered Framework laptops he's used for the past two years.",

    "https://linuxblog.io/linux-server-diy-projects-for-beginners/":
        "A practical guide introducing Linux newcomers to hands-on server projects spanning virtualisation, server management, and security. Designed to build real Linux skills through experimentation rather than theory alone.",

    "http://softwaredoug.com/blog/2026/04/06/agentic-search-is-having-a-grep-moment.html":
        "Doug Turnbull explores whether plain grep can power agentic AI search, concluding it's technically feasible but far from trivial. The post reflects on the trade-offs between simplicity and sophistication when building retrieval for autonomous agents.",

    "https://www.poppastring.com/blog/three-new-mai-models":
        "Microsoft announced three new MAI (Microsoft AI) models, expanding its lineup of AI language models available to enterprise and developer audiences.",

    "https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/":
        "Microsoft released v1.0 of its Agent Framework, providing a stable foundation for developers building AI-agent applications on the Microsoft platform.",

    "https://jeremydmiller.com/2026/04/03/wolverine-gap-analysis/":
        "Jeremy Miller performs a gap analysis of the Wolverine messaging and command-bus framework for .NET, identifying areas for improvement or missing functionality in the current release.",

    "https://devblogs.microsoft.com/oldnewthing/20260403-00/?p=112202":
        "Raymond Chen explains how to use the Windows ReadDirectoryChangesW API to detect when files are being copied out of a directory, addressing a nuanced edge case in file-system monitoring.",

    "https://www.simplethread.com/building-a-ux-research-brain-atomic-research-zettelkasten-and-obsidian/":
        "The article tackles \"Research Amnesia\"—the recurring loss of past user research insights in product teams—by proposing a system combining Atomic Research methodology with a Zettelkasten approach in Obsidian. The result is a persistent, searchable UX knowledge base that survives team and project turnover.",

    "https://devblogs.microsoft.com/aspire/aspire-docs-in-your-terminal/":
        "Covers how to surface .NET Aspire documentation directly in your terminal and feed it into AI coding assistants, keeping developers in-flow without switching to a browser.",

    "https://devblogs.microsoft.com/azure-sdk/azure-developer-cli-azd-march-2026/":
        "The March 2026 Azure Developer CLI update adds local run-and-debug support for AI agents, tighter GitHub Copilot integration, and Container App Jobs support—streamlining AI development and deployment workflows on Azure.",

    "https://dirkstrauss.com/claude-code-windows-migration-guide/":
        "A step-by-step guide for migrating a complete Claude Code setup—MCP servers, slash commands, plugins, and access rules—to a new Windows machine. Addresses the common pain of losing configuration files during hardware upgrades.",

    "https://www.bennadel.com/blog/4884-unified-coldfusion-custom-tag-traversal-in-cfml-engines.htm":
        "Ben Nadel demonstrates a unified technique for traversing the ColdFusion custom tag stack across Adobe ColdFusion, Lucee, and BoxLang, carefully handling the platform-specific quirks of each engine.",

    # Engineering Blogs
    "https://www.tigerdata.com/blog/how-hardware-affects-iiot-workloads":
        "Explores how RAM, storage, and CPU choices directly affect the three-constraint IIoT performance envelope (storage capacity, ingest rate, query speed). Shows how doubling hardware resources can shift what workloads a database can comfortably handle.",

    "https://realpython.com/quizzes/for-loop-python/":
        "An interactive quiz from Real Python testing knowledge of Python for-loops, including iterables, iterators, set iteration order, and the behaviour of break and continue.",

    "https://blogs.windows.com/windows-insider/2026/04/03/announcing-windows-11-insider-preview-build-26220-8148-beta-channel/":
        "Microsoft released Windows 11 Insider Preview Build 26220.8148 to the Beta Channel, delivering incremental fixes and improvements ahead of broader rollout.",

    "https://blogs.windows.com/windows-insider/2026/04/03/announcing-windows-11-insider-preview-build-26300-8155-dev-channel/":
        "Build 26300.8155 arrives in the Dev Channel, giving Windows Insiders early access to features and changes currently under active development.",

    "https://blogs.windows.com/windows-insider/2026/04/03/announcing-windows-11-insider-preview-build-for-canary-channel-29560-1000/":
        "Build 29560.1000 lands in the Canary Channel—the most experimental Windows Insider ring—previewing cutting-edge changes furthest from general availability.",

    "https://blogs.windows.com/windows-insider/2026/04/03/announcing-windows-11-insider-preview-build-28020-1803-canary-channel/":
        "Another Canary Channel release (28020.1803), continuing Microsoft's rapid experimental iteration cycle for the most adventurous Windows testers.",

    "https://blog.jetbrains.com/rust/2026/04/03/rustrover-2026-1-professional-testing-with-native-cargo-nextest-integration/":
        "JetBrains released RustRover 2026.1 with native cargo-nextest integration, bringing a professional-grade, fast test runner experience directly into the Rust IDE.",

    # AI & ML Blogs
    "https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/new-and-improved-multi-agent-orchestration-connected-experiences-and-faster-prompt-iteration/":
        "Microsoft announced Copilot Studio updates featuring enhanced multi-agent orchestration, improved connected-experience integrations, and faster prompt iteration tooling for enterprise AI developers.",

    "https://simonwillison.net/2026/Apr/3/cognitive-cost/#atom-everything":
        "Simon Willison explores how AI coding agents affect developer cognition, examining both the cognitive offloading benefits and the subtler risks of increasingly autonomous code generation.",

    "https://simonwillison.net/2026/Apr/3/supply-chain-social-engineering/#atom-everything":
        "An analysis of a supply chain attack targeting the Axios JavaScript library, notable for using individually crafted social engineering rather than bulk phishing—making it significantly harder to detect.",

    "https://simonwillison.net/2026/Apr/6/google-ai-edge-gallery/#atom-everything":
        "Simon Willison reviews Google's AI Edge Gallery iPhone app, which runs Gemma 4 models fully on-device. The compact E2B model (2.54 GB) is fast and capable, supporting image Q&A and 30-second audio transcription.",

    "https://simonwillison.net/2026/Apr/6/datasette-ports-2/#atom-everything":
        "datasette-ports 0.2 removes the hard dependency on a full Datasette install—it can now run standalone via uvx—while continuing to work as an optional Datasette plugin.",

    "https://simonwillison.net/2026/Apr/6/scan-for-secrets/#atom-everything":
        "scan-for-secrets 0.3 adds a --redact option that interactively confirms matches and replaces them with \"REDACTED\" in files, plus a new Python API for programmatic redaction.",

    "https://simonwillison.net/2026/Apr/6/cleanup-claude-code-paste/#atom-everything":
        "A small utility that removes the extra whitespace artifacts produced when copying prompts from the Claude Code terminal app—solving a niche but persistent formatting annoyance.",

    "https://openai.com/index/industrial-policy-for-the-intelligence-age":
        "OpenAI outlines its vision for people-first industrial policy in the AI era, focusing on expanding economic opportunity, sharing AI-generated prosperity broadly, and building resilient institutions to manage the transition to advanced AI.",

    "https://simonwillison.net/2026/Apr/6/datasette-ports/#atom-everything":
        "The initial release of datasette-ports, a tool Simon Willison built to track and list all running Datasette instances across terminal windows—solving his personal problem of losing them in a sea of sessions.",

    "https://simonwillison.net/2026/Apr/5/building-with-ai/#atom-everything":
        "Lalit Maganti's long-form account of building syntaqlite—a comprehensive SQLite linting and verification tool—describes how AI assistance compressed eight years of wanting the project into three months of actual construction. Simon Willison calls it one of the best pieces of long-form agentic engineering writing he's read.",

    "https://simonwillison.net/2026/Apr/5/chengpeng-mou/#atom-everything":
        "Shares anonymised ChatGPT usage data from OpenAI's Head of Business Finance: ~2M weekly messages on health insurance and ~600K healthcare messages from people in hospital deserts, with 70% occurring outside clinic hours—highlighting AI's emerging role as a healthcare access point.",

    "https://blog.langchain.com/continual-learning-for-ai-agents/":
        "LangChain argues that AI agent learning should be understood across three distinct layers—model weights, the agent harness, and context—rather than focusing solely on fine-tuning. This reframe changes how developers should architect systems that genuinely improve over time.",

    "https://simonwillison.net/2026/Apr/5/syntaqlite/#atom-everything":
        "Simon Willison compiled Lalit Maganti's syntaqlite SQLite linter to WebAssembly via Pyodide and wrapped it in a browser playground, making the tool instantly accessible without any installation.",

    # Top Tech Blogs
    "https://github.blog/engineering/architecture-optimization/the-uphill-climb-of-making-diff-lines-performant/":
        "GitHub's engineering team documents the iterative challenges of making diff-line rendering fast at scale, covering architecture decisions, profiling findings, and the performance bottlenecks they overcame.",

    "https://go.theregister.com/feed/www.theregister.com/2026/04/06/windows_asks_a_networking_question/":
        "The Register's Bork!Bork!Bork! column covers a Windows network-connectivity dialog that escaped onto a public billboard in Stratford—a colourful reminder that public displays and OS prompts shouldn't mix.",

    "https://go.theregister.com/feed/www.theregister.com/2026/04/06/who_me/":
        "A reader-contributed \"Who, Me?\" confession about a developer whose cold-weather arrival triggered a thermal event that melted a mainframe—one of The Register's trademark Monday-morning cautionary tales.",

    "https://go.theregister.com/feed/www.theregister.com/2026/04/06/anthropic_code_leak_kettle_podcast/":
        "The Register's Kettle podcast dissects the reputational and IPO-related fallout from Anthropic's accidental release of Claude Code's source code, examining what it means for the company's public positioning.",

    # Product
    "https://www.lennysnewsletter.com/p/anthropics-1b-to-19b-growth-run":
        "Amol Avasare joins Lenny's Podcast to detail how Anthropic scaled Claude from a $1B to $19B valuation, covering the product strategy and go-to-market decisions that made it the fastest-growing AI product ever.",
}

# ── Category colour palette ────────────────────────────────────────────────
CAT_COLORS = {
    "Leadership":        "#4a90d9",
    "Politics":          "#d94a4a",
    "Agile":             "#e8a838",
    "Engineering":       "#4ab56e",
    "Engineering Blogs": "#7b61d9",
    "AI & ML Blogs":     "#d94ab5",
    "Top Tech Blogs":    "#29b8cc",
    "Product":           "#88b840",
}
DEFAULT_COLORS = ["#4a90d9","#d94a4a","#e8a838","#4ab56e","#7b61d9","#d94ab5","#29b8cc","#88b840"]

def cat_color(cat, idx):
    return CAT_COLORS.get(cat, DEFAULT_COLORS[idx % len(DEFAULT_COLORS)])

def safe(t):
    return html.escape(str(t) if t else "")

def slug(cat):
    return re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')

# ── Deduplicate by link (keep first occurrence) ───────────────────────────
seen_links = set()
deduped_cats = {}
for cat, items in cats.items():
    unique = []
    for item in items:
        lnk = item.get("link","")
        if lnk not in seen_links:
            seen_links.add(lnk)
            unique.append(item)
    if unique:
        deduped_cats[cat] = unique

total_items = sum(len(v) for v in deduped_cats.values())
n_cats = len(deduped_cats)
n_feeds = stats["feeds_fetched"]
n_errors = stats["feeds_errored"]
digest_extracted = stats["digest_articles_extracted"]

# ── Build HTML ─────────────────────────────────────────────────────────────
parts = []

parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Feed Digest: {DATE}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f0f2f5;color:#1a1a2e;line-height:1.6}}
  .wrap{{max-width:720px;margin:0 auto;padding:16px}}
  /* Header */
  .header{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);color:#fff;border-radius:12px;padding:32px 28px 24px;margin-bottom:20px}}
  .header h1{{font-size:1.6rem;font-weight:700;letter-spacing:-.5px}}
  .header .date{{font-size:1rem;opacity:.75;margin-top:4px}}
  .stats{{display:flex;gap:20px;margin-top:18px;flex-wrap:wrap}}
  .stat{{background:rgba(255,255,255,.12);border-radius:8px;padding:8px 14px;text-align:center}}
  .stat-val{{font-size:1.4rem;font-weight:700}}
  .stat-lbl{{font-size:.72rem;opacity:.8;text-transform:uppercase;letter-spacing:.5px}}
  /* TOC */
  .toc{{background:#fff;border-radius:12px;padding:20px 22px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.07)}}
  .toc h2{{font-size:.8rem;text-transform:uppercase;letter-spacing:.8px;color:#888;margin-bottom:12px}}
  .toc-pills{{display:flex;flex-wrap:wrap;gap:8px}}
  .toc-pill{{display:inline-block;padding:5px 14px;border-radius:20px;font-size:.82rem;font-weight:600;color:#fff;text-decoration:none;opacity:.92;transition:opacity .15s}}
  .toc-pill:hover{{opacity:1}}
  /* Category cards */
  .cat-card{{background:#fff;border-radius:12px;padding:22px 22px 16px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.07);border-left:4px solid #ccc}}
  .cat-title{{font-size:1.05rem;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px}}
  .cat-count{{font-size:.75rem;font-weight:500;background:#f0f2f5;border-radius:12px;padding:2px 9px;color:#666}}
  /* Items */
  .item{{padding:12px 0;border-bottom:1px solid #f0f2f5}}
  .item:last-child{{border-bottom:none;padding-bottom:0}}
  .item-title{{font-weight:700;font-size:.95rem;margin-bottom:2px}}
  .item-title a{{color:#1a1a2e;text-decoration:none}}
  .item-title a:hover{{text-decoration:underline}}
  .item-meta{{font-size:.78rem;color:#999;margin-bottom:5px}}
  .item-summary{{font-size:.87rem;color:#444;line-height:1.55}}
  .overflow-note{{font-size:.8rem;color:#888;font-style:italic;margin-top:10px;padding-top:8px;border-top:1px dashed #e0e0e0}}
  /* Footer */
  .footer{{background:#fff;border-radius:12px;padding:18px 22px;margin-top:8px;box-shadow:0 1px 3px rgba(0,0,0,.07);font-size:.83rem;color:#666;text-align:center}}
  .footer strong{{color:#444}}
</style>
</head>
<body>
<div class="wrap">

<div class="header">
  <div class="date">Daily Digest</div>
  <h1>{DATE}</h1>
  <div class="stats">
    <div class="stat"><div class="stat-val">{total_items}</div><div class="stat-lbl">Articles</div></div>
    <div class="stat"><div class="stat-val">{n_feeds}</div><div class="stat-lbl">Feeds checked</div></div>
    <div class="stat"><div class="stat-val">{n_cats}</div><div class="stat-lbl">Categories</div></div>
    <div class="stat"><div class="stat-val">{digest_extracted}</div><div class="stat-lbl">Digest links extracted</div></div>
  </div>
</div>

<div class="toc">
  <h2>Contents</h2>
  <div class="toc-pills">
""")

for idx, cat in enumerate(deduped_cats.keys()):
    color = cat_color(cat, idx)
    parts.append(f'    <a class="toc-pill" href="#{slug(cat)}" style="background:{color}">{safe(cat)} ({len(deduped_cats[cat])})</a>\n')

parts.append("  </div>\n</div>\n\n")

# Category sections
for idx, (cat, items) in enumerate(deduped_cats.items()):
    color = cat_color(cat, idx)
    overflow_n = len(overflow.get(cat, []))
    parts.append(f'<div class="cat-card" id="{slug(cat)}" style="border-left-color:{color}">\n')
    parts.append(f'  <div class="cat-title" style="color:{color}">{safe(cat)} <span class="cat-count">{len(items)} items</span></div>\n')

    for item in items:
        link = item.get("link","")
        title = item.get("title","(no title)")
        feed = item.get("feed_name","")
        summary = SUMMARIES.get(link, "")
        if not summary:
            summary = f"Article from {safe(feed)} covering {safe(title.lower())}."

        parts.append(f"""  <div class="item">
    <div class="item-title"><a href="{safe(link)}" target="_blank" rel="noopener">{safe(title)}</a></div>
    <div class="item-meta">{safe(feed)}</div>
    <div class="item-summary">{safe(summary)}</div>
  </div>
""")

    if overflow_n:
        parts.append(f'  <div class="overflow-note">+{overflow_n} more items not shown (cap reached)</div>\n')

    parts.append('</div>\n\n')

# Footer
parts.append(f"""<div class="footer">
  <strong>{n_feeds}</strong> feeds checked &nbsp;·&nbsp; <strong>{n_errors}</strong> unreachable &nbsp;·&nbsp; Generated {DATE}
</div>

</div>
</body>
</html>
""")

html_content = "".join(parts)
out = f"{DATE}.html"
with open(out, "w") as f:
    f.write(html_content)

print(f"Written {out} ({len(html_content):,} bytes, {total_items} items, {n_cats} categories)")
