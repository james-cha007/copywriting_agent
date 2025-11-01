from core.llm_config import get_llm_model
from core.prompt_templates import build_prompt
from core.validation import validate_and_fix, verify_and_adjust_banners
from core.utils import safe_parse_json, extract_display_data
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()


class CardAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.8):
        self.llm = get_llm_model(model_name, temperature=temperature)

    def run(self, n_variation: int, objective_text: str, campaign_detail: str, product_text: str, example_block: str):
        messages = build_prompt(n_variation, objective_text, campaign_detail, product_text, example_block)

        # Using the model directly with system+user messages
        raw = self.llm.generate([{"role": "system", "content": messages["system"]}, {"role": "user", "content": messages["user"]}])

        # Pull text from the model response - adjust to your client library
        llm_text = raw.generations[0][0].text if hasattr(raw, "generations") else raw

        # Parse JSON safely (attempts basic fixes)
        parsed = safe_parse_json(llm_text)

        # Validate and normalize
        normalized = validate_and_fix(parsed)
        verified = verify_and_adjust_banners({"items": normalized})

        # Final display
        display_json = extract_display_data(verified)
        return display_json