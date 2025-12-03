import os
import pytest
from app.chatbot_agent import ChatbotAgent


@pytest.mark.asyncio
async def test_chatbot_agent_fallback_without_llm():
    os.environ["USE_LLM"] = "false"
    agent = ChatbotAgent()

    class Input:
        def __init__(self):
            self.messages = [{"role": "user", "content": "Explique Better Agents"}]

    result = await agent.call(Input())
    assert result["role"] == "assistant"
    assert "Explique" in result.get("content", "")
