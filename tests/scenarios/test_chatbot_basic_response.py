import pytest
from app.chatbot_agent import ChatbotAgent


@pytest.mark.asyncio
async def test_chatbot_agent_basic_response():
    agent = ChatbotAgent()

    class Input:
        def __init__(self):
            self.messages = [{"role": "user", "content": "Olá, quem é você?"}]

    result = await agent.call(Input())
    assert result["role"] == "assistant"
    assert isinstance(result.get("content"), str) and len(result.get("content")) > 0
