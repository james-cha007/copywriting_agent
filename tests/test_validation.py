from core.validation import _normalize_text, _verify_field, validate_and_fix
from core.prompt_templates import build_prompt
import json

def test_normalize_text():
    assert _normalize_text("  a  b \n") == "a b"

def test_verify_field_trims_length():
    s, issues = _verify_field("สวัสดี" * 50)
    assert any(i["type"] == "length_trimmed" for i in issues)

def test_validate_and_fix_structure():
    model_json = [{"title": "ทดสอบ", "subtitle": "ข้อความ"}]
    cleaned = validate_and_fix(model_json)
    assert isinstance(cleaned, list)
    assert all("title" in x and "subtitle" in x for x in cleaned)

def test_build_prompt_contains_fields():
    prompts = build_prompt(3, "objective", "campaign", "product", "example")
    assert "system" in prompts and "user" in prompts
    assert "objective" in prompts["user"]
