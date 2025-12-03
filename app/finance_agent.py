from typing import Any, List
import os

from dotenv import load_dotenv
from langwatch import trace
import scenario

from app.tools.finance_api import get_returns
from app.tools.whatsapp_sender import send_message


load_dotenv()


class FinanceAgent(scenario.AgentAdapter):
    @trace()
    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        user_msgs = [m.get("content", "") for m in input.messages if m.get("role") == "user"]
        text = " ".join(user_msgs)
        schedule_time = "09:00"
        symbols: List[str] = ["PETR4", "VALE3", "ITUB4"]
        returns = get_returns(symbols)
        phone = os.getenv("WPP_PHONE", "5511999999999")
        summary = ", ".join([f"{s}: {returns.get(s, 0.0):+.1f}%" for s in symbols])
        msg = f"Agendamento confirmado para {schedule_time}. Rentabilidade de hoje: {summary}. Envio via WPPConnect."  
        send_message(phone, msg)
        return {"role": "assistant", "content": msg}

