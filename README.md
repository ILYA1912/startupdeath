# 💀 StartupDeath

> **6 brutal AI agents destroy your startup idea in 30 seconds.**
> 
> **[→ Try it live: startupdeath.onrender.com](https://startupdeath.onrender.com)**

![kills](https://img.shields.io/badge/ideas%20killed-1247-red)
![license](https://img.shields.io/badge/license-MIT-orange)
![powered by](https://img.shields.io/badge/powered%20by-Groq%20%2B%20Llama%203.3-blue)
![free](https://img.shields.io/badge/AI%20cost-$0-green)

---

## The problem

Your friend spent 2 years and $60,000 on a startup.

It had a fatal flaw on day 1. Nobody told him.

---

## What StartupDeath does

You type your idea. In 30 seconds, 6 AI agents attack it simultaneously from every angle — and produce a **Certificate of Startup Death** with a **Survival Score (0–100)**.

The lower the score, the closer to death.

Every idea is saved in the **public Startup Graveyard** — a growing database of killed ideas anyone can browse.

---

## The 6 Killers

| Agent | What they destroy |
|-------|-------------------|
| 💰 **Skeptical Investor** | Your financials, TAM, unit economics |
| 😴 **Lazy Customer** | Why they'll never open their wallet |
| 😈 **Ruthless Competitor** | How Google, Amazon, or a $5M-funded rival kills you |
| 🏛️ **Regulator & Lawyer** | Every law, license, and GDPR clause that shuts you down |
| 😤 **Burnt-out Employee** | The internal chaos that destroys you from inside |
| 📉 **Pessimist Analyst** | Why your timing is completely wrong |

---

## What makes it different from ChatGPT

**Real failure database.** Every agent has access to 30 documented startup failures — with names, amounts raised, and exact cause of death. Your idea gets compared to real companies that died doing the same thing.

```
"Uber for Groceries" → Agent references Webvan ($800M raised, dead in 36 months)
"AI Health Diagnostics" → Agent references Theranos ($700M raised, founder jailed)  
"On-demand Laundry" → Agent references Washio ($16.5M raised, dead in 36 months)
```

**Startup Graveyard.** Every destroyed idea is added to a public database. You can browse 1000+ killed ideas, see Survival Scores, and find what categories die fastest.

**Survival Score.** A number from 0 to 100. Specific. Shareable. Brutal.

---

## Example output

```
Input: "Uber for dogs — on-demand dog walking app"

💰 INVESTOR:   "DogVacay raised $47M and sold for scraps. Rover survived only because 
               they raised $300M. You have neither the runway nor the differentiation."

😴 CUSTOMER:   "I already use Rover. Why would I switch? Your network effects start 
               at zero. I need walkers in my neighborhood. You have none."

😈 COMPETITOR: "Rover will undercut your price the moment you get traction. They have 
               3M registered sitters. You have a landing page."

📊 SURVIVAL SCORE: 12/100
⏱️  TIME TO DEATH: 8 months
💀 CAUSE: No moat. Rover kills you in quarter 2.
```

---

## Tech stack

- **Backend:** Python + FastAPI
- **AI:** Groq API + Llama 3.3 70B — **completely free**
- **Frontend:** Vanilla HTML/CSS/JS — zero dependencies, zero frameworks
- **Database:** JSON flat files (graveyard.json, kill_count.json)
- **Deploy:** Render.com free tier

**Total AI cost to run: $0.** Groq's free tier handles everything.

---

## Run locally in 2 minutes

```bash
git clone https://github.com/ILYA1912/startupdeath
cd startupdeath

pip install -r backend/requirements.txt

# Get a free Groq API key at console.groq.com (takes 30 seconds)
echo "GROQ_API_KEY=your_key_here" > backend/.env

cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Open http://localhost:8000
```

No paid API keys. No database setup. No Docker. No config files.

---

## Deploy to Render (free)

1. Fork this repo
2. Go to [render.com](https://render.com) → New Web Service → Connect your fork
3. Add `GROQ_API_KEY` environment variable
4. Deploy. Done.

---

## Startup Graveyard

Every analysis is saved to a public graveyard at `/graveyard`.

Browse the data:
- **Total kills** — how many ideas have died
- **Survival Score distribution** — what scores are most common
- **Category breakdown** — which startup categories die fastest
- **Recent kills feed** — last 30 ideas destroyed, with causes

The graveyard grows with every user. This is the data moat.

---

## Features

- [x] 6 parallel AI agents (run simultaneously, not sequentially)
- [x] Real failure database — 30 real startups, with amounts raised and cause of death
- [x] Survival Score 0–100
- [x] Certificate of Death (shareable image)
- [x] Startup Graveyard (public database of all kills)
- [x] Category tagging and analytics
- [ ] Resurrection mode — agents flip and tell you how to fix each fatal flaw
- [ ] Compare two ideas head to head
- [ ] API access for developers
- [ ] Slack / Notion integration

---

## Star the repo

If this saved you from a bad idea — or if you just enjoyed watching someone else's idea die:

⭐ **Star this repo** — it helps other founders find it

🐦 **Share your Survival Score** on Twitter

💀 **[Try it live](https://startupdeath.onrender.com)**

---

Built by a solo founder who watched too many friends burn their savings on bad ideas.

MIT License — free to use, fork, and deploy.
