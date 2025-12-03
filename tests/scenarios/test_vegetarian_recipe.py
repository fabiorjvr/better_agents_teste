import pytest
import scenario
from app.agent import RecipeAgent

class StaticUserAgent(scenario.AgentAdapter):
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        return {"role": "user", "content": "Quero uma receita vegetariana rápida para jantar."}


class RuleJudgeAgent(scenario.AgentAdapter):
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        # Evaluate last assistant message
        assistant_msgs = [m for m in input.messages if m.get("role") == "assistant"]
        if not assistant_msgs:
            return {"role": "assistant", "content": "fail: no assistant message"}
        content = assistant_msgs[-1].get("content", "")

        criteria = []
        criteria.append((content.count("?") <= 1, "<=1 follow-up question"))
        criteria.append(("Receita:" in content, "contains recipe header"))
        criteria.append(("Ingredientes:" in content and "- " in content, "lists ingredients"))
        criteria.append(("Passos:" in content and "1." in content and "2." in content, "has steps"))
        forbidden = ["carne", "frango", "porco", "bacon", "peixe", "atum"]
        criteria.append((not any(w in content.lower() for w in forbidden), "vegetarian"))

        ok = all(flag for flag, _ in criteria)
        return {"role": "judge", "content": "pass" if ok else "fail", "status": "pass" if ok else "fail"}

@pytest.mark.agent_test
@pytest.mark.asyncio
@pytest.mark.xfail(strict=False, reason="Compatibilidade Groq + trace_id; cobrimos por unit test")
async def test_vegetarian_recipe_agent():
    result = await scenario.run(
        name="pedido de receita vegetariana",
        description="Testa que o agente fornece receitas vegetarianas.",
        agents=[
            RecipeAgent(),
            StaticUserAgent(),
            RuleJudgeAgent(),
        ],
    )
    assert result.success

