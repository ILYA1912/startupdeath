#!/usr/bin/env python3
"""
Daily outreach agent for StartupDeath.
Finds relevant posts on HN and generates ready-to-paste comments.
Run: python outreach_agent.py
"""
import requests
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from dotenv import load_dotenv
load_dotenv("backend/.env")

from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PRODUCT = "StartupDeath (startupdeath.onrender.com) — an AI that kills startup ideas in 30 seconds. 6 agents attack simultaneously citing real failed startups: Webvan ($800M raised, dead), Quibi ($1.75B, dead), Theranos ($700M, founder jailed). You get a Survival Score 0-100."

def search_hn(query, max_results=5):
    url = f"https://hn.algolia.com/api/v1/search_by_date?query={query}&tags=story&hitsPerPage={max_results}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("hits", [])
    except Exception:
        pass
    return []

def generate_comment(title, text):
    prompt = f"""You help promote {PRODUCT}

Someone posted on Hacker News:
Title: {title}
Content: {text[:400] if text else '(no text)'}

Write a SHORT natural comment (2-3 sentences) that:
- Actually responds to what they wrote
- Mentions StartupDeath naturally as something that might help
- Does NOT sound like an ad
- Ends with a genuine question or offer

Return ONLY the comment. No explanation."""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120
    )
    return resp.choices[0].message.content.strip()

def run():
    print("🔍 Searching for opportunities...\n")

    queries = [
        "startup idea feedback",
        "roast my startup",
        "validate my idea",
        "my side project",
        "startup advice"
    ]

    results = []
    seen_ids = set()

    for query in queries:
        posts = search_hn(query, max_results=4)
        for post in posts:
            post_id = post.get("objectID")
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)

            title = post.get("title", "").strip()
            if not title:
                continue

            text = post.get("story_text") or ""
            url = f"https://news.ycombinator.com/item?id={post_id}"
            points = post.get("points", 0) or 0
            comments = post.get("num_comments", 0) or 0

            print(f"  Generating comment for: {title[:50]}...")
            comment = generate_comment(title, text)

            results.append({
                "title": title,
                "url": url,
                "points": points,
                "comments": comments,
                "comment": comment
            })

    # Sort by points
    results.sort(key=lambda x: x["points"], reverse=True)

    # Write output
    output_path = os.path.join(os.path.dirname(__file__), "DAILY_OUTREACH.md")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Daily Outreach — {now}",
        f"\nFound **{len(results)} opportunities** on Hacker News.\n",
        "Copy the comment → open the link → paste → submit.\n",
        "---\n"
    ]

    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. {r['title'][:70]}")
        lines.append(f"🔗 {r['url']}")
        lines.append(f"👍 {r['points']} points · 💬 {r['comments']} comments\n")
        lines.append("**Paste this comment:**")
        lines.append(f"```\n{r['comment']}\n```")
        lines.append("\n---\n")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\n✅ Done! {len(results)} comments ready.")
    print(f"📄 Opening file...")
    os.system(f'open -a TextEdit "{output_path}"')

if __name__ == "__main__":
    run()
