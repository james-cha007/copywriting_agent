import json
from typing import Any, Dict, List


def extract_display_data(gen_chain_output: Dict[str, Any]) -> str:
    items_list = gen_chain_output.get("items", [])
    display = [
        {"card_no": item.get("card_id"), "title": item.get("title"), "subtitle": item.get("subtitle")}
        for item in items_list
    ]
    return json.dumps(display, ensure_ascii=False, indent=2)


def safe_parse_json(text: str) -> Any:
    """Try to parse JSON, with simple fixes for common LLM mistakes (trailing commas, single quotes)."""
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        # lightweight fixes
        fixed = text.replace("\'", '"')
        fixed = fixed.replace(r",\n\s*\]", "\n]")
        try:
            return json.loads(fixed)
        except Exception:
            raise