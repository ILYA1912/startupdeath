# StartupDeath — Launch Guide

## Утром (5 минут):

### 1. Пополни баланс
→ console.anthropic.com → Billing → Add $5

### 2. Запусти сервер
Открой Терминал и введи:
```
cd ~/Desktop/StartupDeath/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Открой приложение
Открой браузер и перейди на:
```
http://localhost:8000
```

### 4. Протестируй
Введи идею: "Uber for dogs" → нажми Kill My Idea

---

## Для публикации в интернет:

### Railway (бесплатный хостинг):
1. Зайди на railway.app
2. Подключи GitHub аккаунт
3. Загрузи папку StartupDeath
4. Добавь переменную ANTHROPIC_API_KEY в настройках
5. Получи публичный URL

---

## Первые посты для запуска:

**Twitter/X:**
"I built an AI that destroys your startup idea in 30 seconds.
6 brutal agents: investor, customer, competitor, regulator, employee, analyst.
All tell you why you'll fail.
Free. No signup.
💀 startupde.ath"

**Reddit (r/startups, r/entrepreneur):**
"I got tired of people hyping bad startup ideas, so I built StartupDeath.
6 AI agents destroy your idea from every angle.
Brutally honest. Free. Takes 30 seconds.
Would love your feedback."

**Product Hunt:**
Название: StartupDeath
Tagline: 6 AI agents kill your startup idea in 30 seconds
