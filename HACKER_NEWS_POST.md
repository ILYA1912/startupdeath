# Hacker News — Show HN Post

## Заголовок (точно так):
Show HN: I built an AI that kills startup ideas in 30 seconds (using real failure data)

## Текст (вставить в поле "text"):

My friend spent 2 years and $40,000 on a startup. It had a fatal flaw on day 1. Nobody told him because nobody wanted to be the one to kill his dream.

I built StartupDeath to be that person.

**How it works:**

You type your idea. 6 AI agents attack it simultaneously from every angle — investor, customer, competitor, regulator, employee, analyst. They run in parallel, not sequentially, so the whole thing takes ~30 seconds.

**What makes it different from just asking ChatGPT:**

Each agent has access to a database of 30 documented startup failures — with exact amounts raised, months survived, and cause of death. So instead of generic advice, you get:

"You're building the same thing as Webvan ($800M raised, dead in 36 months). Their infrastructure costs destroyed them at exactly the scale you're targeting."

**The Startup Graveyard:**

Every analyzed idea gets saved to a public database with a Survival Score (0–100). You can browse all killed ideas, see what categories die fastest, and find the most common causes of death. It's growing into a dataset of what actually kills startups — not theory, but pattern matching against real failures.

**Tech:**
- FastAPI + Groq (Llama 3.3 70B) — completely free API
- Vanilla HTML/CSS/JS frontend
- Deployed on Render free tier
- Total cost to run: $0

**Repo:** https://github.com/ILYA1912/startupdeath
**Live:** https://startupdeath.onrender.com

Happy to run anyone's startup idea in the comments. Drop it below.

---

## КАК ПОСТИТЬ:

1. Перейди на: https://news.ycombinator.com/submit
2. Title: Show HN: I built an AI that kills startup ideas in 30 seconds (using real failure data)
3. URL: https://startupdeath.onrender.com
4. Text: вставь текст выше
5. Нажми "submit"

**ЛУЧШЕЕ ВРЕМЯ:** 8-10 утра по EST (Нью-Йорк) = 16-18:00 по UAE
Сегодня это: ~16:00 по Dubai time

---

## Почему это сработает на HN:

- Developers любят "I built X in N days" посты
- "Using real failure data" — конкретная техническая деталь
- Groq + Llama = бесплатно запустить локально = разработчики будут пробовать
- "Drop your idea in the comments" — генерирует комментарии = больше апвоутов
- HN любит честность: "nobody wanted to be the one to kill his dream"
