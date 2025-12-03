import json
from pathlib import Path
from typing import Optional

import yaml


def load_prompt_by_id(prompt_id: str) -> Optional[str]:
    registry_path = Path("prompts.json")
    if not registry_path.exists():
        return None
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    prompts = data.get("prompts", [])
    match = next((p for p in prompts if p.get("id") == prompt_id), None)
    if not match:
        return None
    yaml_path = Path(match.get("path", ""))
    if not yaml_path.exists():
        return None
    content = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    prompt = content.get("prompt")
    return prompt

