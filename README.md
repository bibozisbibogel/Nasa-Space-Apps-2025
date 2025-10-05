 🚀 Go/No-Go Advisor — Launch Readiness AI App

## 🧠 Overview
This project is a **Launch Go/No-Go Advisor** — an AI-powered system that determines whether conditions are favorable for launching the **Big Refueler** rocket into Low Earth Orbit (LEO).

It uses:
- **Meteomatics Weather API** → to get real-time and forecast weather data (wind, clouds, precipitation, temperature).
- **NOAA SWPC API** → to check **space weather conditions** (solar storms, Kp index).
- **Space-Track API** → to check for **debris/conjunction (COLA)** risks.

The app provides a simple interface where you:
1. **Select a launch site** from the dropdown (e.g., Kennedy Space Center, Vandenberg SFB)
2. **Pick a date and time** using the calendar picker

The system then analyzes the conditions and responds with:
```json
{
  "verdict": "MARGINAL",
  "risk_score": 58,
  "why": "Cloud thickness near the 4,500 ft LLCC limit; Kp elevated at 6...",
  "rule_citations": [
    "NASA-STD-4010A §4.1.8 (Thick Cloud Layers)",
    "Vehicle SOP: Pad Wind Limit 30 kn",
    "SWPC Kp advisory"
  ]
}


## Documentation for APIs

📡 Meteomatics Weather API

Getting Started / Intro: “Getting started with the Meteomatics Weather API” — REST usage, examples, etc. - https://www.meteomatics.com/en/api/getting-started/?utm_source=chatgpt.com


Advanced request types, route queries, etc. (“Advanced Requests”) - https://www.meteomatics.com/en/api/request/advanced-requests/?utm_source=chatgpt.com

API Tutorials / how to use it (parameters, URL format) - https://www.meteomatics.com/en/api/api-tutorials/?utm_source=chatgpt.com 
also https://www.youtube.com/watch?v=IzmST1Lht3c

Available parameters list (alphabetical) - https://www.meteomatics.com/en/api/available-parameters/alphabetic-list/?utm_source=chatgpt.com


Python connector / library interface to Meteomatics - https://github.com/meteomatics/python-connector-api?utm_source=chatgpt.com

☀️ NOAA SWPC (Space Weather Prediction Center) API / Data Service

Data Access overview: SWPC’s “Data Access” page describing the JSON and product service endpoints - https://www.swpc.noaa.gov/content/data-access?utm_source=chatgpt.com

JSON index / directory listing of products under services.swpc.noaa.gov/json/ - https://services.swpc.noaa.gov/json/?utm_source=chatgpt.com

Products & Data overview (catalog of what SWPC offers) - https://www.swpc.noaa.gov/products-and-data?utm_source=chatgpt.com

Real-time solar wind JSON format description - https://www.swpc.noaa.gov/products/real-time-solar-wind?utm_source=chatgpt.com

🛰️ Space-Track.org API Documentation

Official “Help Documentation / API” page on Space-Track site - https://www.space-track.org/documentation?utm_source=chatgpt.com

Python client (spacetrack library) docs (interface and usage) - https://spacetrack.readthedocs.io/en/stable/?utm_source=chatgpt.com

Handbook / operator documentation (context / usage) - https://www.space-track.org/documents/Spacetrack_Handbook_for_Operators.pdf?utm_source=chatgpt.com

## Front-end + Back-end

Backend: Python 3.11+, FastAPI + Uvicorn, httpx

Front-end: Next.js + Tailwind (thin SPA that calls /api/decide)

Caching: In-memory (per-process) for 2–5 minutes to avoid hammering APIs

Auth: none

## 📁 Folder Structure - This helps Claude place each file where it belongs.

├── backend/
│ ├── api.py
│ ├── decide.py
│ ├── sites.py
│ └── integrations/
│ ├── meteomatics.py
│ ├── swpc.py
│ └── spacetrack.py
└── frontend/
├── app/page.tsx
├── lib/api.ts
├── tailwind.config.js
├── globals.css
└── ...

## 🧩 How to Run

### 1. Backend

**Setup virtual environment and install dependencies:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Configure environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Meteomatics API credentials
```

**Run the server:**
```bash
source venv/bin/activate  # If not already activated
uvicorn api:app --reload --port 8000
```

### 2. Frontend

**Install dependencies and run:**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser!