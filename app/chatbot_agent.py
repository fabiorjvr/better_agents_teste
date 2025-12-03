from typing import Any
import os

from dotenv import load_dotenv
from langwatch import trace
import scenario

from app.prompt_loader import load_prompt_by_id


load_dotenv()


def _sanitize_messages(msgs: list[dict]) -> list[dict]:
    return [{"role": m.get("role"), "content": m.get("content", "")} for m in msgs]


class ChatbotAgent(scenario.AgentAdapter):
    @trace()
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        system_prompt = load_prompt_by_id("chatbot_system") or "Você é um Chatbot útil."
        use_llm = os.getenv("USE_LLM", "true").lower() == "true"
        if use_llm:
            try:
                import litellm
                model = os.getenv("MODEL_NAME") or "groq/llama-3.1-70b-instant"
                messages = [{"role": "system", "content": system_prompt}, *_sanitize_messages(input.messages)]
                resp = litellm.completion(model=model, messages=messages)
                msg: Any = resp.choices[0].message
                return msg
            except Exception:
                pass
        last_user = next((m.get("content", "") for m in input.messages if m.get("role") == "user"), "")
        return {"role": "assistant", "content": f"Entendi: {last_user}"}

