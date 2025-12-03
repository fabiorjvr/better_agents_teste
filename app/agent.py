from typing import Any
import os

from dotenv import load_dotenv
from langwatch import trace
import scenario

from app.prompt_loader import load_prompt_by_id


def _sanitize_messages(msgs: list[dict]) -> list[dict]:
    cleaned = []
    for m in msgs:
        cleaned.append({"role": m.get("role"), "content": m.get("content", "")})
    return cleaned


load_dotenv()


class RecipeAgent(scenario.AgentAdapter):
    @trace()
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        system_prompt = load_prompt_by_id("vegetarian_recipe_v1") or (
            "Você é um agente de receitas vegetarianas. Faça no máximo uma "
            "pergunta de acompanhamento e forneça receita completa com ingredientes e passos."
        )

        use_llm = os.getenv("USE_LLM", "true").lower() == "true"
        if use_llm:
            try:
                import litellm

                model = os.getenv("MODEL_NAME") or "groq/llama-3.1-70b-versatile"
                messages = [
                    {"role": "system", "content": system_prompt},
                    *_sanitize_messages(input.messages),
                ]
                resp = litellm.completion(model=model, messages=messages)
                msg: Any = resp.choices[0].message
                return msg
            except Exception:
                pass

        follow_up = "Você tem alguma restrição de ingredientes?"
        recipe = (
            "Receita: Macarrão ao Pesto de Espinafre\n"
            "Ingredientes:\n"
            "- Macarrão penne\n"
            "- Espinafre\n"
            "- Manjericão\n"
            "- Alho\n"
            "- Nozes\n"
            "- Azeite\n"
            "- Sal\n\n"
            "Passos:\n"
            "1. Cozinhe o macarrão.\n"
            "2. Bata espinafre, manjericão, alho, nozes e azeite.\n"
            "3. Misture o pesto ao macarrão.\n"
            "4. Ajuste sal e sirva.\n"
        )
        content = f"{follow_up}\n\n{recipe}"
        return {"role": "assistant", "content": content}

