import os
import asyncio
import json
import re
from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

COUNTER_FILE = "kill_count.json"
WAITLIST_FILE = "waitlist.json"
GRAVEYARD_FILE = "graveyard.json"

def get_kill_count():
    try:
        with open(COUNTER_FILE) as f:
            return json.load(f).get("total", 0)
    except:
        return 0

def increment_kill_count():
    count = get_kill_count() + 1
    with open(COUNTER_FILE, "w") as f:
        json.dump({"total": count}, f)
    return count

def load_graveyard():
    try:
        with open(GRAVEYARD_FILE) as f:
            return json.load(f)
    except:
        return {"startups": []}

def save_to_graveyard(idea: str, category: str, survival_score: int, cause_of_death: str, time_to_death: str):
    data = load_graveyard()
    entry = {
        "id": len(data["startups"]) + 1,
        "idea_preview": idea[:60] + ("..." if len(idea) > 60 else ""),
        "category": category,
        "survival_score": survival_score,
        "cause_of_death": cause_of_death,
        "time_to_death": time_to_death,
        "killed_at": str(date.today())
    }
    data["startups"].append(entry)
    with open(GRAVEYARD_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return entry

def load_waitlist():
    try:
        with open(WAITLIST_FILE) as f:
            return json.load(f)
    except:
        return []

def save_email(email: str):
    waitlist = load_waitlist()
    if email not in waitlist:
        waitlist.append(email)
        with open(WAITLIST_FILE, "w") as f:
            json.dump(waitlist, f)
    return len(waitlist)

AGENTS = [
    {
        "name": "💰 Skeptical Investor",
        "role": "You are a legendary Silicon Valley VC who has seen 10,000 pitches and funded 12. You're brutal because you've watched founders waste their life savings. Find specific financial fatal flaws: unrealistic CAC, no path to profitability, wrong market size assumptions. Name real competitors and their funding. End with 'VERDICT:' and one brutal sentence that would make a founder cry."
    },
    {
        "name": "😴 Lazy Customer",
        "role": "You are the exact target customer for this product. You're busy, skeptical, and already have 5 apps you don't use. Be brutally specific about why you'd never pay for this — what habit it requires you to break, what's your current free alternative, why you'd forget about it after day 3. End with 'VERDICT:' and one honest sentence."
    },
    {
        "name": "😈 Ruthless Competitor",
        "role": "You are the CEO of the dominant player in this market. You have 500 engineers, $200M in cash, and you've crushed 47 startups. Describe your exact counter-attack: which feature you'll clone in 2 weeks, how much you'll spend to outrank them on Google, which of their engineers you'll poach with 2x salary. End with 'VERDICT:' and one sentence."
    },
    {
        "name": "🏛️ Regulator & Lawyer",
        "role": "You are a senior government regulator and corporate lawyer with 25 years of experience shutting down startups. Find every legal landmine: specific laws they're likely violating, licenses they don't know they need, GDPR/CCPA issues, liability exposure. Give real dollar amounts for fines. End with 'VERDICT:' and one sentence."
    },
    {
        "name": "😤 Burnt-out Employee",
        "role": "You are employee #3 at this startup. It's month 9. Payroll was late twice. The product roadmap changed 4 times. The founder micromanages everything and sleeps 4 hours. Describe the specific internal chaos unfolding right now — the Slack arguments, the feature creep, the tech debt that's paralyzing the team. End with 'VERDICT:' and one sentence."
    },
    {
        "name": "📉 Pessimist Analyst",
        "role": "You are a senior market analyst at Goldman Sachs. Prove with specific data why this startup is entering at the worst possible moment: market saturation stats, macro headwinds, consumer behavior shifts, regulatory changes coming, or why the window of opportunity already closed. Be precise with numbers. End with 'VERDICT:' and one sentence."
    }
]

RESURRECTION_AGENTS = [
    {
        "name": "💰 Investor Fix",
        "role": "You are the same brutal VC, but now you're coaching the founder. Based on the financial fatal flaws you identified, give ONE specific pivot that makes the unit economics work. Be concrete: different pricing model, different customer segment, different go-to-market. End with 'THE FIX:' and one actionable sentence."
    },
    {
        "name": "😴 Customer Unlock",
        "role": "You are the lazy customer who just said no. Now tell the founder the ONE thing that would make you immediately pull out your credit card. What pain is so bad you'd pay to fix it? What would make this a must-have instead of nice-to-have? End with 'THE FIX:' and one actionable sentence."
    },
    {
        "name": "😈 Competitor Gap",
        "role": "You are the dominant competitor CEO. You just admitted you'd crush them — but there's ONE thing you can't do because you're too big, too slow, or too regulated. That's the gap the startup should own. Identify it precisely. End with 'THE FIX:' and one actionable sentence."
    },
    {
        "name": "🏛️ Legal Path",
        "role": "You are the same lawyer. Now tell the founder the fastest legal path to launch without getting sued — what to do first, what license to get, which market to start in to avoid the biggest regulations. End with 'THE FIX:' and one actionable sentence."
    },
    {
        "name": "😤 Team Structure",
        "role": "You are the burnt-out employee. Tell the founder exactly what they must do differently to retain the team: which decisions to delegate, what process to add, what toxic behavior to stop. End with 'THE FIX:' and one actionable sentence."
    },
    {
        "name": "📉 Timing Pivot",
        "role": "You are the market analyst. The timing is wrong for the original idea — but point to an adjacent market or problem where the timing is perfect right now. Use real trends. End with 'THE FIX:' and one actionable sentence."
    }
]

class StartupRequest(BaseModel):
    idea: str
    description: str = ""
    resurrection: bool = False

class EmailRequest(BaseModel):
    email: str

def parse_summary_fields(text: str):
    score_match = re.search(r'SURVIVAL SCORE:\s*(\d+)', text, re.IGNORECASE)
    category_match = re.search(r'CATEGORY:\s*([^\n]+)', text, re.IGNORECASE)
    cause_match = re.search(r'MAIN CAUSE OF DEATH:\s*([^\n]+)', text, re.IGNORECASE)
    time_match = re.search(r'TIME TO DEATH:\s*([^\n]+)', text, re.IGNORECASE)
    return {
        "survival_score": min(100, max(0, int(score_match.group(1)))) if score_match else 25,
        "category": category_match.group(1).strip().split("/")[0].strip() if category_match else "Other",
        "cause_of_death": cause_match.group(1).strip() if cause_match else "Multiple fatal flaws",
        "time_to_death": time_match.group(1).strip() if time_match else "12 months"
    }

def run_agent_sync(agent: dict, idea: str, description: str) -> dict:
    prompt = f"""Startup idea: {idea}
{"Description: " + description if description else ""}

{agent['role']}

Write 2-3 sharp paragraphs. Be specific and brutal."""

    msg = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"agent": agent["name"], "verdict": msg.choices[0].message.content}

async def run_agent(agent: dict, idea: str, description: str) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, run_agent_sync, agent, idea, description)

@app.get("/api/stats")
async def get_stats():
    return {"total": get_kill_count(), "waitlist": len(load_waitlist())}

@app.get("/api/graveyard")
async def get_graveyard():
    data = load_graveyard()
    startups = data["startups"]

    if not startups:
        return {"total": 0, "avg_score": 0, "categories": {}, "category_avg_scores": {}, "recent": []}

    categories = {}
    cat_scores = {}
    for s in startups:
        cat = s.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1
        cat_scores.setdefault(cat, []).append(s.get("survival_score", 25))

    scores = [s.get("survival_score", 25) for s in startups]
    avg_score = round(sum(scores) / len(scores), 1)
    cat_avg = {cat: round(sum(v) / len(v), 1) for cat, v in cat_scores.items()}

    return {
        "total": len(startups),
        "avg_score": avg_score,
        "categories": categories,
        "category_avg_scores": cat_avg,
        "recent": list(reversed(startups[-30:]))
    }

@app.post("/api/waitlist")
async def join_waitlist(req: EmailRequest):
    count = save_email(req.email)
    return {"success": True, "position": count}

@app.post("/api/analyze")
async def analyze(request: StartupRequest):
    tasks = [run_agent(a, request.idea, request.description) for a in AGENTS]
    results = await asyncio.gather(*tasks)

    summary_prompt = f"""Startup idea: "{request.idea}"

Six brutal experts just destroyed this startup. Write a Certificate of Death using EXACTLY this format:

SURVIVAL SCORE: [single number 0-100, where 0=dead on arrival, 100=unicorn. Most ideas score 10-40]
CATEGORY: [pick exactly one: SaaS / Marketplace / Consumer App / EdTech / FinTech / HealthTech / E-commerce / Media / Hardware / Other]
MAIN CAUSE OF DEATH: [one savage sentence — the #1 fatal flaw]
TIME TO DEATH: [X months, be specific, range 2-18]
CAUSE #2: [second killer]
CAUSE #3: [third killer]
FOUNDER'S LAST WORDS: "[darkly funny quote the founder would actually say]"
AUTOPSY NOTES: [one sentence of dark humor]

Be brutal, specific, and memorable. No generic statements."""

    loop = asyncio.get_event_loop()
    summary_msg = await loop.run_in_executor(None, lambda: client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=350,
        messages=[{"role": "user", "content": summary_prompt}]
    ))

    summary_text = summary_msg.choices[0].message.content
    parsed = parse_summary_fields(summary_text)

    resurrection_results = None
    if request.resurrection:
        res_tasks = [run_agent(a, request.idea, request.description) for a in RESURRECTION_AGENTS]
        resurrection_results = list(await asyncio.gather(*res_tasks))

    increment_kill_count()
    graveyard_entry = save_to_graveyard(
        request.idea,
        parsed["category"],
        parsed["survival_score"],
        parsed["cause_of_death"],
        parsed["time_to_death"]
    )

    return {
        "idea": request.idea,
        "agents": list(results),
        "summary": summary_text,
        "survival_score": parsed["survival_score"],
        "category": parsed["category"],
        "graveyard_id": graveyard_entry["id"],
        "resurrection": resurrection_results
    }

@app.get("/api/config")
async def get_config():
    stripe_link = os.getenv("STRIPE_PAYMENT_LINK", "")
    return {"stripe_link": stripe_link}

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
