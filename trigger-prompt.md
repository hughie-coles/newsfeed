# Daily Feed Digest — CCR Trigger Prompt

Run the daily RSS feed digest pipeline and create a Gmail draft with the results.

## Steps

1. Set up the environment:
```bash
cd /home/user/newsfeed
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Fetch feeds and generate JSON:
```bash
python3 fetch_feeds.py --output digest.json
```

3. Build HTML digest with AI summaries:
```bash
python3 build_digest.py --input digest.json --output digest.html
```

4. Read the generated HTML and create a Gmail draft:
- Read the file `digest.html`
- Get today's date for the subject line
- Create a Gmail draft to hughie.coles@gmail.com with:
  - Subject: "Feed Digest: YYYY-MM-DD" (using today's date)
  - Body: the full HTML content from digest.html
  - Content type: text/html

## Important

- Run the Python scripts exactly as shown above. Do NOT generate HTML yourself.
- If `build_digest.py` fails (e.g., missing API key), still create the draft using the JSON data — read digest.json and build a simple HTML summary manually as a fallback.
- The Gmail draft should NOT be sent automatically — just create the draft.
