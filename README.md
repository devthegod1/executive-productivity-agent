# How to Run the Project

## 1. Setup API Key
Create a `.env` file in the root directory:
```env
MISTRAL_API_KEY="your_actual_mistral_api_key_here"
MISTRAL_MODEL=open-mistral-7b
SIMULATED_NOW=2026-09-24T17:00:00

## 2. Run the Web Application
uv run streamlit run src/agent/app.py

3. Run the Tests
uv run pytest

4. Run via Terminal (CLI Query)
uv run python -c "from agent.core import ExecutiveProductivityAgent; agent = ExecutiveProductivityAgent(); print(agent.answer_question('When do I owe Raghav the vendor list?')[0])"
