from typing import Dict


def send_message(phone: str, message: str) -> Dict[str, str]:
    return {"status": "queued", "provider": "stub", "phone": phone}

