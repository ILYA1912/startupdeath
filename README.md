# 💀 StartupDeath

> **6 brutal AI agents destroy your startup idea in 30 seconds.**

![StartupDeath Demo](https://img.shields.io/badge/status-live-red)
![License](https://img.shields.io/badge/license-MIT-orange)
![Made with Claude](https://img.shields.io/badge/powered%20by-Claude%20AI-red)

---

## What is StartupDeath?

You have a startup idea. You think it's brilliant.

StartupDeath sends it through **6 ruthless AI agents** who attack it from every angle simultaneously — and produce a full **Certificate of Startup Death** in 30 seconds.

Better to know now than after spending your savings.

---

## The 6 Killers

| Agent | Role |
|-------|------|
| 💰 **Skeptical Investor** | Destroys your financials and market size |
| 😴 **Lazy Customer** | Explains why they'll never buy |
| 😈 **Ruthless Competitor** | Shows exactly how they'll crush you |
| 🏛️ **Regulator & Lawyer** | Finds every law that will shut you down |
| 😤 **Burnt-out Employee** | Reveals the internal chaos that kills you |
| 📉 **Pessimist Analyst** | Proves your timing is completely wrong |

---

## Demo

```
Input:  "Uber for dogs"

Output: 
CAUSE OF DEATH: Unit economics impossible at any scale
TIME OF DEATH:  4 months
LAST WORDS:     "But dogs LOVE our app..."
```

---

## Quick Start

### Requirements
- Python 3.9+
- Node.js 18+
- Anthropic API key ([get one here](https://console.anthropic.com))

### Run locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/startupdeath
cd startupdeath

# Install dependencies
pip install -r backend/requirements.txt

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > backend/.env

# Start the server
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Open in browser
open http://localhost:8000
```

---

## Tech Stack

- **Backend:** Python + FastAPI
- **Frontend:** Vanilla HTML/CSS/JS (zero dependencies)
- **AI:** Claude claude-haiku-4-5-20251001 (fast + cheap)
- **Deploy:** Railway / Render / any VPS

---

## Deploy to Railway (1 click)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click the button above
2. Add `ANTHROPIC_API_KEY` environment variable
3. Get your public URL in 2 minutes

---

## Self-hosted vs Cloud

| Feature | Self-hosted (free) | Cloud ($9/mo) |
|---------|-------------------|---------------|
| Run locally | ✅ | ✅ |
| Your own API key | ✅ | ❌ not needed |
| Public URL | ❌ set up yourself | ✅ instant |
| Updates | manual | ✅ automatic |
| Support | community | ✅ priority |

---

## Roadmap

- [x] 6 AI agents analysis
- [x] Certificate of Death
- [x] Share to Twitter/LinkedIn
- [ ] Save and share results via URL
- [ ] Compare two ideas
- [ ] Team mode (invite co-founders)
- [ ] API access for developers
- [ ] Slack / Notion integration

---

## Contributing

PRs welcome! Check [CONTRIBUTING.md](CONTRIBUTING.md)

If you found a bug or have an idea — open an issue.

---

## License

MIT — free to use, modify, and deploy.

---

## Support the project

If StartupDeath saved you from a bad idea:

- ⭐ Star this repo
- 🐦 Share on Twitter
- ☕ [Buy me a coffee](https://buymeacoffee.com)
- 💼 [Try the cloud version](https://startupdeath.app)

---

Built with 💀 and Claude AI
