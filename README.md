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

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Sudhanshu9336/ai_public_health_chatbot_whatsapp_telegram.git
cd ai_public_health_chatbot_whatsapp_telegram
```

2. Configure environment variables:
```bash
# Copy and edit environment files
cp services/backend/.env.example services/backend/.env
# Edit .env with your API keys (WhatsApp/Telegram/Gemini)
```

3. Build and run with Docker:
```bash
docker compose up --build
```

Services will be available at:
- Frontend Dashboard: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Rasa Server: http://localhost:5005

### Local Development Setup

1. **Rasa Setup**:
```bash
# Terminal 1 - Rasa API
cd services/rasa
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
rasa train
rasa run --enable-api --cors "*" -p 5005

# Terminal 2 - Rasa Actions
cd services/rasa
.\.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # Linux/Mac
rasa run actions -p 5055
```

2. **Backend Setup**:
```bash
cd services/backend
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. **Frontend Setup**:
```bash
cd services/frontend
npm install
npm run dev
```

### Environment Configuration

1. Backend (.env):
```ini
WHATSAPP_CLOUD_TOKEN=your_token
TELEGRAM_BOT_TOKEN=your_bot_token
RASA_BASE_URL=http://localhost:5005
GEMINI_API_KEY=your_gemini_key
```

2. For WhatsApp Cloud API:
- Set up a Meta Developer account
- Configure webhook URL to `https://<your-host>/webhook/whatsapp`
- Add `WHATSAPP_CLOUD_TOKEN` to .env

3. For Telegram:
- Create a bot with @BotFather
- Set webhook: `https://api.telegram.org/bot<token>/setWebhook?url=https://<your-host>/webhook/telegram`
- Add `TELEGRAM_BOT_TOKEN` to .env

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

