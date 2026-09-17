import json
from typing import List, Tuple
try:
    from mistralai import Mistral
except ImportError:
    from mistralai.client import Mistral
from agent.config import config
from agent.tools import TOOL_DEFINITIONS, TOOL_MAP

class MistralAgentRunner:
    def __init__(self, api_key: str = "", model: str = ""):
        self.api_key = api_key or config.MISTRAL_API_KEY
        self.model = model or config.MISTRAL_MODEL
        self.client = Mistral(api_key=self.api_key) if self.api_key else None

    def execute_chat(self, messages: List[dict]) -> Tuple[str, List[str], List[str]]:
        if not self.client:
            raise ValueError("MISTRAL_API_KEY is not set. Add it to .env.")

        citations = []
        reasoning_trace = []
        conversation = list(messages)

        while True:
            response = self.client.chat.complete(
                model=self.model,
                messages=conversation,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto"
            )
            msg = response.choices[0].message
            tool_calls = msg.tool_calls

            if not tool_calls:
                final_text = msg.content or ""
                return final_text, citations, reasoning_trace

            conversation.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    } for tc in tool_calls
                ]
            })

            for tc in tool_calls:
                fn_name = tc.function.name
                raw_args = tc.function.arguments
                if isinstance(raw_args, str):
                    try:
                        fn_args = json.loads(raw_args) if raw_args.strip() else {}
                    except Exception:
                        fn_args = {}
                elif isinstance(raw_args, dict):
                    fn_args = raw_args
                else:
                    fn_args = {}
                reasoning_trace.append(f"Invoked tool `{fn_name}` with args `{fn_args}`")
                fn = TOOL_MAP.get(fn_name)
                result = fn(**fn_args) if fn else {"error": f"Unknown tool: {fn_name}"}

                # Record citations from tool calls
                if fn_name == "search_emails":
                    for item in result:
                        citations.append(f"Email Thread: '{item.get('thread')}' (Seq {item.get('seq')}, {item.get('datetime')})")
                elif fn_name == "get_voice_notes":
                    for vn in result:
                        citations.append(f"Voice Note: {vn.get('id')} ({vn.get('datetime')})")
                elif fn_name == "get_transcript":
                    citations.append("Transcript: leadership_sync_2026-09-21")
                elif fn_name == "get_calendar":
                    for cal in result:
                        citations.append(f"Calendar: {cal.get('person')} - {cal.get('day')} {cal.get('time')} ({cal.get('event')})")

                conversation.append({
                    "role": "tool",
                    "name": fn_name,
                    "content": json.dumps(result),
                    "tool_call_id": tc.id
                })