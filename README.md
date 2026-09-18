# Executive Productivity Agent

An autonomous multi-modal executive productivity agent designed to synthesize calendar schedules, multi-thread emails, meeting transcripts, and voice notes into grounded executive briefings and proactive risk alerts[cite: 1].

---

## Features

- **Automated Daily Briefing:** Synthesizes unread messages, commitments, and calendar events against a fixed reference timestamp (`2026-09-24 17:00 IST`)[cite: 1].
- **Chronological Recency Resolution:** Accurately sorts communications chronologically rather than by thread sequence to extract true agreed deadlines (e.g., resolving the Raghav vendor list deadline)[cite: 1].
- **Unowned Risk Detection:** Flags critical commitments lacking designated owners (e.g., the upcoming Mumbai office lease renewal) and identifies calendar scheduling conflicts[cite: 1].
- **Traceable Source Citations:** Emits grounded citation tags for every assertion and executive action item[cite: 1].

---

## LLM Configuration

- **Model:** `mistral-large-latest`[cite: 1, 2]
- **API Provider:** Mistral AI[cite: 1, 2]
- **Execution Mode:** Function / Tool Calling via the official `mistralai` Python SDK[cite: 1, 2]
- **Temperature:** `0.1` (configured for deterministic, grounded reasoning and structured JSON output)[cite: 1, 2]

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
├── pyproject.toml              # Project metadata and package setup
└── README.md