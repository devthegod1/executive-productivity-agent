from agent.config import config
from agent.models import AgentResponse
from agent.prompts import SYSTEM_PROMPT, BRIEFING_USER_PROMPT
from agent.mistral_client import MistralAgentRunner

class ExecutiveProductivityAgent:
    def __init__(self, runner: MistralAgentRunner = None, simulated_now: str = None):
        self.runner = runner or MistralAgentRunner()
        self.simulated_now = simulated_now or config.SIMULATED_NOW

    def _get_system_message(self) -> dict:
        return {
            "role": "system",
            "content": SYSTEM_PROMPT.format(simulated_now=self.simulated_now)
        }

    def answer_question(self, query: str) -> AgentResponse:
        messages = [
            self._get_system_message(),
            {"role": "user", "content": query}
        ]
        text, citations, trace = self.runner.execute_chat(messages)
        # Deduplicate citations while preserving order
        unique_citations = list(dict.fromkeys(citations))
        return AgentResponse(answer=text, citations=unique_citations, reasoning_trace=trace)

    def generate_briefing(self, as_of: str = None) -> AgentResponse:
        target_time = as_of or self.simulated_now
        query = BRIEFING_USER_PROMPT.format(as_of=target_time)
        return self.answer_question(query)