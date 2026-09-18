# Executive Productivity Agent

An autonomous multi-modal executive productivity agent designed to synthesize calendar schedules, multi-thread emails, meeting transcripts, and voice notes into grounded executive briefings and proactive risk alerts.

---

## Features

- **Automated Daily Briefing:** Synthesizes unread messages, commitments, and calendar events against a fixed reference timestamp (`2026-09-24 17:00 IST`).
- **Chronological Recency Resolution:** Accurately sorts communications chronologically rather than by thread sequence to extract true agreed deadlines (e.g., resolving the Raghav vendor list deadline).
- **Unowned Risk Detection:** Flags critical commitments lacking designated owners (e.g., the upcoming Mumbai office lease renewal) and identifies calendar scheduling conflicts.
- **Traceable Source Citations:** Emits grounded citation tags for every assertion and executive action item.

---

## LLM Configuration

- **Model:** `mistral-large-latest`
- **API Provider:** Mistral AI
- **Execution Mode:** Function / Tool Calling via the official `mistralai` Python SDK
- **Temperature:** `0.1` (deterministic, grounded reasoning and structured output)

---

## Project Structure

```text
.
├── data/                       # Ingested datasets (emails, calendar, transcripts, voice notes)
├── src/
│   └── agent/
│       ├── app.py              # Streamlit dashboard interface
│       ├── config.py           # Configuration loader
│       ├── core.py             # Agent orchestration and execution loop
│       ├── data_loader.py      # Schema ingestion and temporal normalizers
│       ├── mistral_client.py   # Mistral API tool-calling integration
│       └── tools.py            # Local search and filtering tool definitions
├── tests/
│   └── test_agent.py           # Automated evaluation test suite
├── pyproject.toml              # Project metadata, build specs, and tool settings
├── requirements.txt            # Pinned dependency manifest
└── README.md

Quickstart (Run in 3 Steps)
1. Set Up Environment & Install Dependencies
Open your terminal in the project directory and run:

## 1. Setup API Key
Create a `.env` file in the root directory:
```env
MISTRAL_API_KEY="your_actual_mistral_api_key_here"
MISTRAL_MODEL=open-mistral-7b
SIMULATED_NOW=2026-09-24T17:00:00

Windows (PowerShell):
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
MISTRAL_API_KEY="your_actual_mistral_api_key_here"
streamlit run src/agent/app.py

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
MISTRAL_API_KEY="your_actual_mistral_api_key_here"
streamlit run src/agent/app.py