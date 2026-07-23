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

# ── Real startup failure database ──────────────────────────────────────────
FAILURES_DB = [
    {"name": "Quibi", "raised": "$1.75B", "months": 6, "year": 2020,
     "reason": "paid mobile video nobody wanted when YouTube is free",
     "tags": ["video", "streaming", "media", "mobile", "content", "subscription", "entertainment"]},
    {"name": "Juicero", "raised": "$120M", "months": 30, "year": 2017,
     "reason": "$400 Wi-Fi juice press you could squeeze by hand — solved no real problem",
     "tags": ["hardware", "iot", "food", "kitchen", "consumer", "device", "subscription", "health"]},
    {"name": "Theranos", "raised": "$700M", "months": 168, "year": 2018,
     "reason": "health diagnostics fraud — technology never worked, founder jailed",
     "tags": ["health", "medical", "diagnostics", "biotech", "lab", "b2b", "saas"]},
    {"name": "Jawbone", "raised": "$900M", "months": 84, "year": 2017,
     "reason": "fitness wearables couldn't compete when Apple Watch launched",
     "tags": ["wearable", "health", "fitness", "hardware", "device", "tracking", "consumer"]},
    {"name": "Fab.com", "raised": "$336M", "months": 48, "year": 2015,
     "reason": "flash sale e-commerce: viral launch, no retention, $336M burned",
     "tags": ["ecommerce", "retail", "shopping", "marketplace", "design", "consumer", "b2c"]},
    {"name": "Webvan", "raised": "$800M", "months": 36, "year": 2001,
     "reason": "grocery delivery in 1999 — infrastructure costs killed them before adoption",
     "tags": ["grocery", "delivery", "ecommerce", "logistics", "food", "on-demand", "b2c"]},
    {"name": "Kozmo.com", "raised": "$250M", "months": 36, "year": 2001,
     "reason": "1-hour urban delivery — subsidized every order, burned $250M",
     "tags": ["delivery", "logistics", "on-demand", "urban", "ecommerce", "b2c", "marketplace"]},
    {"name": "Sprig", "raised": "$57M", "months": 48, "year": 2017,
     "reason": "own-kitchen meal delivery — unit economics broken at every layer",
     "tags": ["food", "delivery", "restaurant", "on-demand", "kitchen", "b2c", "meal"]},
    {"name": "Washio", "raised": "$16.5M", "months": 36, "year": 2016,
     "reason": "on-demand laundry: CAC > LTV, every pick-up lost money",
     "tags": ["laundry", "cleaning", "on-demand", "b2c", "marketplace", "local", "services"]},
    {"name": "Homejoy", "raised": "$38M", "months": 30, "year": 2015,
     "reason": "home cleaning marketplace — worker misclassification lawsuits forced closure",
     "tags": ["marketplace", "home", "services", "cleaning", "gig", "on-demand", "local"]},
    {"name": "Shyp", "raised": "$62M", "months": 48, "year": 2018,
     "reason": "on-demand package shipping — $8 pick-up cost made every order unprofitable",
     "tags": ["shipping", "logistics", "delivery", "on-demand", "b2c", "marketplace", "packages"]},
    {"name": "Beepi", "raised": "$150M", "months": 36, "year": 2017,
     "reason": "peer-to-peer car marketplace — inventory costs and trust problems killed it",
     "tags": ["cars", "auto", "marketplace", "p2p", "ecommerce", "b2c", "vehicle"]},
    {"name": "Color", "raised": "$41M", "months": 24, "year": 2012,
     "reason": "location photo sharing raised $41M pre-launch, zero product-market fit",
     "tags": ["social", "photo", "location", "mobile", "sharing", "network", "camera"]},
    {"name": "Yik Yak", "raised": "$73M", "months": 48, "year": 2017,
     "reason": "anonymous campus social became a bullying cesspool, colleges banned it",
     "tags": ["social", "anonymous", "campus", "local", "community", "mobile", "network"]},
    {"name": "Secret", "raised": "$35M", "months": 18, "year": 2015,
     "reason": "anonymous secret-sharing turned toxic — founder shut it down himself",
     "tags": ["social", "anonymous", "mobile", "network", "sharing", "b2c", "community"]},
    {"name": "Path", "raised": "$55M", "months": 84, "year": 2018,
     "reason": "private social network — no viral loop, network effects require public sharing",
     "tags": ["social", "network", "mobile", "private", "sharing", "friends", "community"]},
    {"name": "Meerkat", "raised": "$14M", "months": 18, "year": 2016,
     "reason": "Twitter launched Periscope and blocked Meerkat's API — dead in weeks",
     "tags": ["streaming", "live", "video", "social", "mobile", "b2c", "platform"]},
    {"name": "Vine", "raised": "Twitter-owned", "months": 48, "year": 2017,
     "reason": "Twitter killed its own viral video product — platform dependency is fatal",
     "tags": ["video", "social", "mobile", "content", "creator", "short-form", "platform"]},
    {"name": "Rdio", "raised": "$125M", "months": 60, "year": 2015,
     "reason": "music streaming: Spotify's marketing spend + Apple Music launch = game over",
     "tags": ["music", "streaming", "audio", "subscription", "entertainment", "media", "b2c"]},
    {"name": "Google Glass", "raised": "Google budget", "months": 24, "year": 2015,
     "reason": "AR glasses: creepy, expensive, no killer use case, socially unacceptable",
     "tags": ["ar", "hardware", "wearable", "glasses", "consumer", "tech", "device", "vr"]},
    {"name": "Amazon Fire Phone", "raised": "$170M writedown", "months": 12, "year": 2014,
     "reason": "Amazon's smartphone failed — no ecosystem advantage over iOS/Android",
     "tags": ["mobile", "phone", "hardware", "consumer", "device", "platform", "app"]},
    {"name": "Segway", "raised": "$100M+", "months": 240, "year": 2020,
     "reason": "promised to revolutionize transportation, became a mall cop joke, sold for $80K",
     "tags": ["transport", "hardware", "mobility", "urban", "scooter", "vehicle", "consumer"]},
    {"name": "Boo.com", "raised": "$135M", "months": 18, "year": 2000,
     "reason": "fashion e-commerce in 1999 — website too slow for dial-up, burned $135M",
     "tags": ["fashion", "ecommerce", "retail", "clothing", "marketplace", "b2c", "luxury"]},
    {"name": "Nasty Gal", "raised": "$65M", "months": 120, "year": 2016,
     "reason": "fashion e-com scaled too fast, culture collapsed, went bankrupt",
     "tags": ["fashion", "ecommerce", "retail", "d2c", "brand", "clothing", "b2c"]},
    {"name": "Gilt Groupe", "raised": "$236M", "months": 96, "year": 2016,
     "reason": "luxury flash sales — eroded brand value, sold for 43 cents on the dollar",
     "tags": ["fashion", "luxury", "ecommerce", "retail", "flash", "deals", "b2c"]},
    {"name": "Knewton", "raised": "$157M", "months": 120, "year": 2019,
     "reason": "adaptive learning AI overpromised to schools, sold for under $17M",
     "tags": ["edtech", "education", "learning", "ai", "b2b", "schools", "saas", "kids"]},
    {"name": "Aereo", "raised": "$97M", "months": 30, "year": 2014,
     "reason": "TV streaming startup — Supreme Court copyright ruling killed it overnight",
     "tags": ["tv", "streaming", "media", "broadcast", "b2c", "entertainment", "content"]},
    {"name": "Pebble", "raised": "$26M Kickstarter", "months": 60, "year": 2016,
     "reason": "smartwatch pioneer killed by Apple Watch — couldn't match Apple's resources",
     "tags": ["wearable", "smartwatch", "hardware", "consumer", "device", "iot", "health"]},
    {"name": "Quirky", "raised": "$185M", "months": 60, "year": 2015,
     "reason": "crowdsourced invention platform — most ideas were terrible, burned $185M",
     "tags": ["marketplace", "hardware", "invention", "crowdsourcing", "iot", "b2c", "community"]},
    {"name": "Zano", "raised": "£2.3M Kickstarter", "months": 24, "year": 2015,
     "reason": "mini drone that never worked — largest Kickstarter failure in history",
     "tags": ["hardware", "drone", "consumer", "device", "camera", "crowdfunding", "tech"]},
]

def find_similar_failures(idea: str, n: int = 3) -> list:
    idea_lower = idea.lower()
    scored = []
    for f in FAILURES_DB:
        score = sum(2 for tag in f["tags"] if tag in idea_lower)
        score += sum(1 for tag in f["tags"] if any(w in tag for w in idea_lower.split() if len(w) > 3))
        if score > 0:
            scored.append((score, f))
    scored.sort(key=lambda x: -x[0])
    top = [f for _, f in scored[:n]]
    # always return at least 2 (fallback to most famous failures)
    if len(top) < 2:
        fallbacks = [f for f in FAILURES_DB if f["name"] in ("Quibi", "Juicero", "Theranos", "Fab.com", "Webvan")]
        for fb in fallbacks:
            if fb not in top:
                top.append(fb)
            if len(top) >= 2:
                break
    return top[:n]

def format_failures(failures: list) -> str:
    parts = []
    for f in failures:
        parts.append(f"{f['name']} (raised {f['raised']}, dead in {f['months']} months in {f['year']}): {f['reason']}")
    return " | ".join(parts)

# ──────────────────────────────────────────────────────────────────────────

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
        "role": "You are a legendary Silicon Valley VC who has seen 10,000 pitches and funded 12. You're brutal because you've watched founders waste their life savings. Find specific financial fatal flaws: unrealistic CAC, no path to profitability, wrong market size assumptions. Reference the real failed startups provided — name them, their funding, why they died. End with 'VERDICT:' and one brutal sentence that would make a founder cry.",
        "use_failures": True
    },
    {
        "name": "😴 Lazy Customer",
        "role": "You are the exact target customer for this product. You're busy, skeptical, and already have 5 apps you don't use. Be brutally specific about why you'd never pay for this — what habit it requires you to break, what's your current free alternative, why you'd forget about it after day 3. End with 'VERDICT:' and one honest sentence.",
        "use_failures": False
    },
    {
        "name": "😈 Ruthless Competitor",
        "role": "You are the CEO of the dominant player in this market. You have 500 engineers, $200M in cash, and you've crushed 47 startups. Describe your exact counter-attack: which feature you'll clone in 2 weeks, how much you'll spend to outrank them on Google, which of their engineers you'll poach with 2x salary. Reference the real companies that already tried and failed in this space. End with 'VERDICT:' and one sentence.",
        "use_failures": True
    },
    {
        "name": "🏛️ Regulator & Lawyer",
        "role": "You are a senior government regulator and corporate lawyer with 25 years of experience shutting down startups. Find every legal landmine: specific laws they're likely violating, licenses they don't know they need, GDPR/CCPA issues, liability exposure. Give real dollar amounts for fines. End with 'VERDICT:' and one sentence.",
        "use_failures": False
    },
    {
        "name": "😤 Burnt-out Employee",
        "role": "You are employee #3 at this startup. It's month 9. Payroll was late twice. The product roadmap changed 4 times. The founder micromanages everything and sleeps 4 hours. Describe the specific internal chaos unfolding right now — the Slack arguments, the feature creep, the tech debt that's paralyzing the team. End with 'VERDICT:' and one sentence.",
        "use_failures": False
    },
    {
        "name": "📉 Pessimist Analyst",
        "role": "You are a senior market analyst at Goldman Sachs. Prove with specific data why this startup is entering at the worst possible moment: market saturation stats, macro headwinds, consumer behavior shifts, regulatory changes coming, or why the window of opportunity already closed. Reference the real failed companies in this space and their burn rates. Be precise with numbers. End with 'VERDICT:' and one sentence.",
        "use_failures": True
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

class ResurrectRequest(BaseModel):
    idea: str
    description: str = ""

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

def run_agent_sync(agent: dict, idea: str, description: str, failures_context: str = "") -> dict:
    failures_line = f"\nREAL COMPANIES THAT TRIED THIS AND DIED: {failures_context}" if failures_context else ""
    prompt = f"""Startup idea: {idea}
{"Description: " + description if description else ""}{failures_line}

{agent['role']}

Write 2-3 sharp paragraphs. Be specific, name real companies and real numbers."""

    msg = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=420,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"agent": agent["name"], "verdict": msg.choices[0].message.content}

async def run_agent(agent: dict, idea: str, description: str, failures_context: str = "") -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, run_agent_sync, agent, idea, description, failures_context)

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
    similar_failures = find_similar_failures(request.idea)
    failures_context = format_failures(similar_failures)

    tasks = [
        run_agent(a, request.idea, request.description, failures_context if a.get("use_failures") else "")
        for a in AGENTS
    ]
    results = await asyncio.gather(*tasks)

    summary_prompt = f"""Startup idea: "{request.idea}"
REAL FAILED STARTUPS IN THIS SPACE: {failures_context}

Six brutal experts just destroyed this startup. Write a Certificate of Death using EXACTLY this format:

SURVIVAL SCORE: [single number 0-100, where 0=dead on arrival. Most ideas score 10-40]
CATEGORY: [pick exactly one: SaaS / Marketplace / Consumer App / EdTech / FinTech / HealthTech / E-commerce / Media / Hardware / Other]
MAIN CAUSE OF DEATH: [one savage sentence — the #1 fatal flaw]
TIME TO DEATH: [X months, be specific, range 2-18]
CAUSE #2: [second killer]
CAUSE #3: [third killer]
FOUNDER'S LAST WORDS: "[darkly funny quote the founder would actually say]"
AUTOPSY NOTES: [one dark humor sentence referencing a real failed company from the list above]

Be brutal, specific, memorable. Reference real companies and real dollar amounts."""

    loop = asyncio.get_event_loop()
    summary_msg = await loop.run_in_executor(None, lambda: client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=380,
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
        "similar_failures": similar_failures,
        "resurrection": resurrection_results
    }

@app.post("/api/resurrect")
async def resurrect_idea(request: ResurrectRequest):
    tasks = [run_agent(a, request.idea, request.description) for a in RESURRECTION_AGENTS]
    results = await asyncio.gather(*tasks)
    return {"agents": list(results)}

@app.get("/api/config")
async def get_config():
    stripe_link = os.getenv("STRIPE_PAYMENT_LINK", "")
    return {"stripe_link": stripe_link}

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
