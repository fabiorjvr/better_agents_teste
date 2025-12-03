import json
from pathlib import Path
import re


SEMVER_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")


def validar():
    registry_path = Path("prompts.json")
    if not registry_path.exists():
        print("❌ prompts.json não encontrado")
        return 1

    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Erro lendo JSON: {e}")
        return 1

    prompts = data.get("prompts", [])
    ok = True
    for p in prompts:
        pid = p.get("id", "").strip()
        name = p.get("name", "").strip()
        model = p.get("model", "").strip()
        version = p.get("version", "").strip()
        file_rel = p.get("file", "").strip()

        if not pid:
            print("❌ Erro em prompt: id vazio")
            ok = False
        if not name:
            print(f"❌ Erro em prompt {pid or '<sem-id>'}: name vazio")
            ok = False
        if not model:
            print(f"❌ Erro em prompt {pid or '<sem-id>'}: model vazio")
            ok = False
        if not SEMVER_RE.match(version):
            print(f"❌ Erro em prompt {pid or '<sem-id>'}: versão inválida '{version}'")
            ok = False
        file_path = Path(file_rel)
        if not file_path.exists():
            print(f"❌ Erro em prompt {pid or '<sem-id>'}: arquivo '{file_rel}' não existe")
            ok = False

    if ok:
        print("✅ prompts.json válido")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(validar())
