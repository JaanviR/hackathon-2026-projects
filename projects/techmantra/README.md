Project Name
Team Members (names and GitHub handles)
Problem Statement – What problem are you solving?
Solution – Describe your solution and how it works.
Tech Stack – Technologies, frameworks, and tools used.
Setup Instructions – How to run your project locally.
Demo – Link to a demo video, live deployment, or screenshots.

# MediTriage — AI Patient Triage Assistant
### CareDevi AI Innovation Hackathon 2026 | Track: AI Patient Triage

---

## The Problem

Every day, patients with serious conditions sit in waiting rooms behind patients with minor complaints — not because doctors don't care, but because there is no intelligent system routing them to the right level of care at the right time. Patients with a stiff neck and high fever wait alongside patients with a runny nose. Every minute of delay in a meningitis case is life-threatening. Every unnecessary ER visit for a common cold wastes resources and delays care for someone who truly needs it.

## What We Built

MediTriage is an AI-powered patient triage assistant that analyzes symptoms using clinical NLP and RAG-grounded LLM inference to route patients to the right care — instantly, safely, and with full source citations.

Patients describe symptoms via text or voice. MediTriage extracts clinical entities, retrieves relevant medical knowledge from trusted sources, runs AI inference grounded exclusively in those sources, and routes the patient to one of three outcomes:

- **LOW risk** — home care with cited remedies from MedlinePlus and CDC
- **MEDIUM risk** — automated doctor appointment booking via Google Calendar
- **HIGH risk** — immediate 911 prompt with emergency call button

Every diagnosis is cited. Every output includes a clinical disclaimer. Patient data never leaves the device.

---

## Architecture

```
Layer 0   Patient signup → FHIR-structured SQLite storage
Layer 1   Symptom input (text or voice via Whisper STT) → medspaCy clinical NER
Layer 2   Preprocessing → structured clinical payload
Layer 2.5 RAG retrieval → LangChain + ChromaDB → MedlinePlus, CDC documents
Layer 3   LLM inference (Mistral via Ollama) → safety-constrained JSON diagnosis
Layer 4   Risk triage engine → LOW / MEDIUM / HIGH decision logic
Layer 5   Output rendering → Streamlit UI + pyttsx3 TTS
Layer 6   Provider summary → Gmail API + Google Calendar appointment booking
Layer 7   Data stores → SQLite + ChromaDB vector store + remedy_db.json
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| LLM | MedGemma via Ollama (local inference) |
| Clinical NER | medspaCy with TargetRule symptom matching |
| RAG Framework | LangChain + ChromaDB |
| Embeddings | pritamdeka/S-PubMedBert-MS-MARCO |
| Database | SQLite (FHIR-structured) |
| STT | OpenAI Whisper (base model, local) |
| TTS | pyttsx3 (local) |
| Notifications | Gmail API |
| Appointments | Google Calendar API |
| Test Data | Synthea synthetic patients |

---

## Key Design Decisions

**Local-first for privacy** — Ollama runs Mistral entirely on-device. No patient symptom data is sent to any external LLM API. This is essential for healthcare applications where data privacy is non-negotiable.

**RAG for safety** — The LLM is instructed to answer only from retrieved medical documents. This prevents hallucination and makes every diagnosis citable. If confidence is below 0.5, the system falls back to "please consult a doctor" rather than guessing.

**medspaCy for clinical accuracy** — General-purpose NLP models miss clinical negation patterns. medspaCy's ConText algorithm correctly handles "patient denies chest pain" and "no fever" — removing negated symptoms from the active symptom list before they reach the LLM.

**FHIR-structured storage** — Patient data is stored in FHIR R4-compatible JSON format within SQLite. This makes the app interoperable with real hospital systems without requiring a separate FHIR server.

**Severity override** — NER keyword detection for emergency symptoms (chest pain, stiff neck, difficulty breathing) always escalates to HIGH risk regardless of LLM confidence score. Safety takes precedence.

---

## Data Sources

All medical knowledge in the RAG pipeline comes from:

- **MedlinePlus** (National Institutes of Health) — consumer health information
- **CDC** (Centers for Disease Control and Prevention) — disease guidelines and emergency symptoms
- **Synthea** — synthetic patient records for testing (no real patient data used)
- **remedy_db.json** — hand-curated home care suggestions sourced from MedlinePlus and CDC

---

## Project Structure

```
projects/
└── techmantra/
│   ├── demo/
│   └── src/  


    ├── app/
    │   ├── main.py                  Streamlit entry point and navigation
    │   └── session_state.py         Global session state management
    ├── pages/
    │   ├── 01_signup.py             Patient profile and physician details
    │   ├── 02_symptoms.py           Symptom input — text and voice
    │   ├── 03_results.py            Diagnosis output and risk routing
    │   └── 04_doctor_dashboard.py   Provider view sorted by urgency
    ├── core/
    │   ├── ner.py                   medspaCy clinical NER pipeline
    │   ├── preprocessing.py         Symptom payload builder
    │   ├── rag.py                   ChromaDB retrieval via LangChain
    │   ├── llm.py                   Ollama Mistral inference
    │   ├── triage.py                Risk engine and remedy lookup
    │   ├── stt.py                   Whisper speech-to-text
    │   └── tts.py                   pyttsx3 text-to-speech
    ├── integrations/
    │   ├── creds_verification.py    Google OAuth handler
    │   ├── calendar.py              Google Calendar appointment booking
    │   ├── notifications.py         Gmail API doctor notifications
    │   └── fhir_builder.py          FHIR resource constructors
    ├── db/
    │   ├── db.py                    SQLite connection and queries
    │   └── remedy_db.json           Home remedy seed data
    ├── rag_data/
    │   ├── ingest.py                Document indexing into ChromaDB
    │   └── sources/                 Medical source text files
    │       ├── cdc/                 CDC guidelines
    │       └── medlineplus/         MedlinePlus articles
    ├── utils/
    │   ├── config.py                Environment variables
    │   └── logger.py                Session audit logging
    ├── docs/
    │   ├── README.md                This file
    │   └── responsible-ai.md        Responsible AI documentation
    ├── test_data/
    │   └── synthea_patients.json    Synthetic test patients
    ├── .env                         API keys — never committed
    └── requirements.txt             All dependencies
```

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com/download) installed
- Google Cloud project with Calendar and Gmail APIs enabled
- `credentials.json` downloaded from Google Cloud Console

### Step 1 — Clone and Install

```bash
git clone https://github.com/your-team/ai-triage-app.git
cd ai-triage-app

python -m venv hackathon
source hackathon/bin/activate      # Mac/Linux
# hackathon\Scripts\activate       # Windows

pip install -r requirements.txt
```

### Step 2 — Pull the LLM

```bash
ollama pull alibayram/medgemma
```

### Step 3 — Initialize Database

```bash
python db/db.py
# Output: Database initialized successfully.
```

### Step 4 — Index Medical Documents

```bash
python rag_data/ingest.py
# Output: All documents indexed into ChromaDB.
```

### Step 5 — Set Up Google Credentials

Place `credentials.json` in the project root, then:

```bash
python integrations/creds_verification.py
# Browser opens for Google login
# token.json is created automatically
```

### Step 6 — Run the App

```bash
streamlit run app/main.py
```

Open `http://localhost:8501` in your browser.

---

## Testing the Pipeline

```bash
# Test NER
python core/ner.py

# Test preprocessing
python core/preprocessing.py

# Test RAG retrieval
python core/rag.py

# Test full LLM pipeline
python core/llm.py

# Test triage engine
python core/triage.py

# Test notifications
python integrations/notifications.py

# Test calendar booking
python integrations/calendar.py
```

---

## Known Limitations

- Ollama performance depends on device hardware — larger models require 16GB+ RAM
- medspaCy TargetRule matching covers defined symptom list only — rare conditions outside the list may not be extracted
- Remedy database covers 10 common conditions — uncommon diagnoses fall back to LLM-generated suggestions
- Google Calendar booking schedules 2 hours from current time as a placeholder — production would require proper scheduling
- Voice input requires clear audio — background noise reduces Whisper accuracy
- The app is a triage aid only — it is not a diagnostic tool and must not be used as a substitute for clinical judgment

---

## Team

| Name | Role | Responsibilities |
|---|---|---|
| Jahnavi | Backend | NER, preprocessing, triage engine, LLM inference, calendar, Gmail notifications |
| Megha | AI & Data | RAG pipeline, database, ChromaDB |
| Harshini | Frontend & Integrations | Streamlit pages, TTS, STT, FHIR builder |

---

## License

Built for CareDevi AI Innovation Hackathon 2026. Not for clinical use.