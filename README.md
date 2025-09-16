# AI-Driven Public Health Chatbot for Disease Awareness (PSID: 25049)

**Organization:** Government of Odisha  
**Department:** Electronics & IT Department  
**Category:** Software  
**Theme:** MedTech / BioTech / HealthTech

## Problem Statement (Provided)
Create a multilingual AI chatbot to educate rural and semi-urban populations about preventive healthcare, disease symptoms, and vaccination schedules. The chatbot should integrate with government health databases and provide real-time alerts for outbreaks.

### Expected Outcome
- A chatbot accessible via WhatsApp or SMS
- Target ≥80% accuracy on health Q&A (with clear disclaimers, safe responses)  
- Increase awareness by ≥20% in target communities (measured via surveys & engagement analytics)

### Technical Feasibility
- Built using NLP frameworks (Rasa OSS 3.x)
- Integrates APIs for government/public health data (Odisha/Govt. MoHFW/open data portals)
- Cloud-deployable (Docker + any cloud VM/Kubernetes)

---

## What’s in this repository?
A full-stack implementation:
- **Rasa** (NLP + Dialogue) — multilingual intents (English/Hindi/Odia), custom actions
- **FastAPI backend** — Twilio (WhatsApp/SMS) webhook, subscriber DB, alert publisher, API adapters
- **React + Tailwind frontend** — clean dashboard for outreach & alerting with excellent UX
- **Data stubs** — vaccine schedule, mock outbreak feed
- **Docker Compose** — one-command local run
- **.env templates** — configure Twilio, DB, Rasa, and API endpoints

> ⚠️ Health safety note: All answers include a disclaimer and point to official sources. This bot does **not** replace a doctor.

---

## Quick Start (Local, no Docker)
1) **Rasa + Actions**
```bash
# terminal 1
cd services/rasa
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
rasa train
rasa run --enable-api --cors "*" -p 5005

# terminal 2 (actions server)
cd services/rasa
source .venv/bin/activate
rasa run actions -p 5055
```

2) **Backend (FastAPI)**
```bash
cd services/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill values
uvicorn app.main:app --reload --port 8000
```

3) **Frontend (React)**
```bash
cd services/frontend
npm i
npm run dev
```

### Twilio WhatsApp/SMS
- In Twilio Console, set the **incoming webhook** to `https://<your-host>/webhook/twilio`
- For local testing, use `ngrok http 8000` and paste the public URL.
- Configure **.env** values from `.env.example` files.

---

## Docker Compose (All-in-one)
```bash
docker compose up --build
```
Services:
- Rasa: `:5005`
- Actions: `:5055`
- Backend: `:8000`
- Frontend: `:5173` (Vite)

---

## Project Structure
```
ai_public_health_chatbot/
├─ README.md
├─ docker-compose.yml
├─ .env.example
├─ data/
│  └─ mock_outbreaks.json
├─ vaccines/
│  └─ vaccine_schedule.json
├─ services/
│  ├─ rasa/
│  │  ├─ requirements.txt
│  │  ├─ config.yml
│  │  ├─ domain.yml
│  │  ├─ credentials.yml
│  │  ├─ endpoints.yml
│  │  ├─ data/
│  │  │  ├─ nlu.yml
│  │  │  ├─ stories.yml
│  │  │  └─ rules.yml
│  │  └─ actions/
│  │     └─ actions.py
│  ├─ backend/
│  │  ├─ requirements.txt
│  │  ├─ .env.example
│  │  └─ app/
│  │     ├─ main.py
│  │     ├─ config.py
│  │     ├─ db.py
│  │     ├─ models.py
│  │     ├─ schemas.py
│  │     └─ twilio_utils.py
│  └─ frontend/
│     ├─ package.json
│     ├─ tsconfig.json
│     ├─ vite.config.ts
│     ├─ postcss.config.js
│     ├─ tailwind.config.ts
│     ├─ index.html
│     ├─ src/
│     │  ├─ main.tsx
│     │  ├─ App.tsx
│     │  ├─ styles.css
│     │  ├─ pages/
│     │  │  ├─ Dashboard.tsx
│     │  │  ├─ Subscribers.tsx
│     │  │  └─ Alerts.tsx
│     │  └─ components/
│     │     ├─ Card.tsx
│     │     ├─ Header.tsx
│     │     └─ LanguageBadge.tsx
└─ Makefile
```

---

## Accuracy, UX & Impact
- **≥80% accuracy**: curated NLU examples, multilingual transformer, fallbacks, clarifying questions, and safe completion.
- **Awareness +20%**: dashboard metrics (reach, unique users), broadcast campaigns, localized content, A/B messaging.
- **Best UX**: large touch targets, language badge, instant opt-in links, dark-ready palette, WCAG AA contrast.

Happy building! 🙌

## Messaging integrations: WhatsApp Cloud API + Telegram (no Twilio required)
This project has been updated to support Meta's **WhatsApp Cloud API** and **Telegram Bot API**.
- For WhatsApp: set `WHATSAPP_PHONE_NUMBER_ID` and `WHATSAPP_CLOUD_TOKEN` in `services/backend/.env`.
- For Telegram: set `TELEGRAM_BOT_TOKEN` and call `https://api.telegram.org/bot<token>/setWebhook` to point to `https://<your-host>/webhook/telegram`.

Incoming webhook endpoints:
- `/webhook/whatsapp` — receive messages from WhatsApp Cloud API
- `/webhook/telegram` — receive messages from Telegram

Outgoing messages use the Cloud API / Telegram Bot API from the backend (no Twilio).

