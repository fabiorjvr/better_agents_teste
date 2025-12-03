import pytest
import scenario
from app.finance_agent import FinanceAgent


class StaticUser(scenario.AgentAdapter):
    async def call(self, input: scenario.AgentInput):
        return {"role": "user", "content": "Quero agendar diário às 9 com PETR4 VALE3 ITUB4"}


@pytest.mark.agent_test
@pytest.mark.asyncio
@pytest.mark.xfail(strict=False, reason="Compatibilidade de JudgeAgent com Groq/Gemini e tracing")
async def test_whatsapp_financas_scenario():
    result = await scenario.run(
        name="whatsapp finanças diário",
        description="Agendar e enviar rentabilidade diária no WhatsApp às 9",
        agents=[
            StaticUser(),
            FinanceAgent(),
        ],
    )
    assert result.success
