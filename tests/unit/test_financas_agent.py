import os
import pytest
from app.finance_agent import FinanceAgent


@pytest.mark.asyncio
async def test_finance_agent_schedules_and_reports():
    os.environ["WPP_PHONE"] = "5511987654321"
    agent = FinanceAgent()

    class Input:
        def __init__(self):
            self.messages = [{"role": "user", "content": "Agendar relatório diário às 9 com PETR4 VALE3 ITUB4"}]

    result = await agent.call(Input())
    assert result["role"] == "assistant"
    content = result["content"]
    assert "Agendamento confirmado para 09:00" in content
    assert "PETR4" in content and "VALE3" in content and "ITUB4" in content
    assert "%" in content
