import os
import asyncio
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Kill counter
COUNTER_FILE = "kill_count.json"

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

AGENTS = [
    {
        "name": "💰 Skeptical Investor",
        "role": "You are a brutal venture capitalist with 20 years of experience watching startups die. Your job: find every financial reason this idea will fail to get funded and collapse. Be specific, reference real market data, name real competitors. End with 'VERDICT:' and one devastating sentence."
    },
    {
        "name": "😴 Lazy Customer",
        "role": "You are the target customer for this product. You are lazy, skeptical, and hate changing your habits. Explain exactly why you would never buy or use this. Be honest and a little cynical. End with 'VERDICT:' and one sentence."
    },
    {
        "name": "😈 Ruthless Competitor",
        "role": "You are the CEO of the biggest company in this space. Explain exactly how you will destroy this startup — copy the idea, undercut on price, outspend on marketing, buy the team. Be ruthless. End with 'VERDICT:' and one sentence."
    },
    {
        "name": "🏛️ Regulator & Lawyer",
        "role": "You are a government regulator and lawyer. Find every legal, compliance, tax, and regulatory problem that will shut this business down. Be specific about laws, fines, and licenses needed. End with 'VERDICT:' and one sentence."
    },
    {
        "name": "😤 Burnt-out Employee",
        "role": "You are employee #1 at this startup, 8 months in. You haven't been paid on time, the product doesn't work as promised, the founder keeps pivoting. Describe the internal chaos that will kill the company. End with 'VERDICT:' and one sentence."
    },
    {
        "name": "📉 Pessimist Analyst",
        "role": "You are a market analyst. Prove that the timing is completely wrong for this product — either the market doesn't exist yet, or it already peaked. Show why macro trends are against this startup. End with 'VERDICT:' and one sentence."
    }
]

class StartupRequest(BaseModel):
    idea: str
    description: str = ""

async def run_agent(agent: dict, idea: str, description: str) -> dict:
    prompt = f"""Startup idea: {idea}
{"Description: " + description if description else ""}

{agent['role']}

Write 2-3 sharp paragraphs. Be specific and brutal."""

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"agent": agent["name"], "verdict": msg.content[0].text}

@app.get("/api/stats")
async def get_stats():
    return {"total": get_kill_count()}

@app.post("/api/analyze")
async def analyze(request: StartupRequest):
    tasks = [run_agent(a, request.idea, request.description) for a in AGENTS]
    results = await asyncio.gather(*tasks)

    summary_prompt = f"""Startup: {request.idea}

Six experts have destroyed this idea. Based on their verdicts, write:

MAIN CAUSE OF DEATH: (one brutal sentence)
TIME OF DEATH: in X months
FOUNDER'S LAST WORDS: "..." (funny/sad quote)

Keep it short, dramatic, and memorable."""

    summary_msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": summary_prompt}]
    )

    increment_kill_count()

    return {
        "idea": request.idea,
        "agents": list(results),
        "summary": summary_msg.content[0].text
    }

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
