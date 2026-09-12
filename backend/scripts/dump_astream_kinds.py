from __future__ import annotations

import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

src = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src))

from services.llm_service import build_llm, configure_models_api_key  # noqa: E402
from paths import SECRETS_PATH  # noqa: E402
from services.langgraph_service import ChatboxdAgent  # noqa: E402
from api.events import events_from_langgraph  # noqa: E402


async def dump(prompt: str, model: str = "gemini-3.8-flash") -> None:
    load_dotenv(SECRETS_PATH)
    configure_models_api_key()
    agent = ChatboxdAgent(llm=build_llm("Google", model), language="ES")
    kinds: Counter[str] = Counter()
    mapped_types: Counter[str] = Counter()
    samples: list[dict] = []
    async for raw in agent.run_async(prompt, thread_id="probe-langchain"):
        kind = raw.get("event") if isinstance(raw, dict) else type(raw).__name__
        kinds[str(kind)] += 1
        if isinstance(raw, dict) and len(samples) < 8:
            samples.append(
                {
                    "event": raw.get("event"),
                    "name": raw.get("name"),
                    "data_keys": sorted((raw.get("data") or {}).keys())
                    if isinstance(raw.get("data"), dict)
                    else type(raw.get("data")).__name__,
                    "top_keys": sorted(raw.keys()),
                }
            )
        for mapped in events_from_langgraph(raw if isinstance(raw, dict) else {}, "ES"):
            mapped_types[mapped.type] += 1
    print("event_kinds=" + json.dumps(dict(kinds), ensure_ascii=False))
    print("mapped_types=" + json.dumps(dict(mapped_types), ensure_ascii=False))
    print("samples=" + json.dumps(samples, ensure_ascii=False, indent=2))


def main() -> int:
    prompt = sys.argv[1] if len(sys.argv) > 1 else "hola"
    asyncio.run(dump(prompt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
