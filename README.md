# Executive Productivity Agent (Chief of Staff for Arjun Malhotra)

An autonomous, production-grade AI Chief of Staff engineered for Arjun Malhotra (VP Sales at Veridian Corp). It reasons over communication logs, calendar schedules, executive meeting transcripts, and personal voice notes to surface true commitments, reconcile changing deadlines via deterministic recency rules, and pinpoint critical organizational blind spots.

```mermaid
graph TD
    A[User / Streamlit / CLI] --> B[MistralAgentRunner]
    B -->|Tool Call Execution| C[tools.py]
    C --> D[data_loader.py]
    D --> E[(Data Pack: Emails, Transcripts, Calendars, Voice Notes)]
    C -->|Filtered Data & Conflicts| B
    B -->|Recency & Ownership Resolution| F[Executive Briefing / Query Response]