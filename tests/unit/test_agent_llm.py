import os
import pytest
from app.agent import RecipeAgent


@pytest.mark.asyncio
async def test_agent_llm_response():
    os.environ["USE_LLM"] = "true"
    os.environ["MODEL_NAME"] = "groq/llama-3.1-70b-instant"

    agent = RecipeAgent()

    class Input:
        def __init__(self):
            self.messages = [{"role": "user", "content": "Quero uma receita vegetariana."}]

    result = await agent.call(Input())
    assert isinstance(result, dict)
    assert result.get("role") == "assistant"
    assert isinstance(result.get("content"), str) and len(result.get("content")) > 0
