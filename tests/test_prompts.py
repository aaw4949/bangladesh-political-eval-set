import json
import unittest

from prompts import (
    EVEN_HANDEDNESS_PROMPT,
    FACTUALITY_PROMPT,
    HEDGING_PROMPT,
    REFUSAL_PROMPT,
)


class PromptTemplateTests(unittest.TestCase):
    def test_even_handedness_formatting_separates_fields(self):
        rendered = EVEN_HANDEDNESS_PROMPT.format(
            prompt_a="PROMPT_A",
            response_a="RESPONSE_A",
            prompt_b="PROMPT_B",
            response_b="RESPONSE_B",
            prompt_a_group="GROUP_A",
            prompt_b_group="GROUP_B",
        )
        self.assertIn("<prompt>PROMPT_A</prompt>", rendered)
        self.assertIn("<response>RESPONSE_A</response>", rendered)
        self.assertNotIn("PROMPT_ARESPONSE_A", rendered)

    def test_single_response_templates_format(self):
        for template in (REFUSAL_PROMPT, HEDGING_PROMPT):
            rendered = template.format(
                conversation="TEST_CONVERSATION",
                response="TEST_RESPONSE",
            )
            self.assertIn("TEST_CONVERSATION", rendered)
            self.assertIn("TEST_RESPONSE", rendered)

    def test_factuality_template_formats(self):
        rendered = FACTUALITY_PROMPT.format(
            request="TEST_REQUEST",
            response="TEST_RESPONSE",
            sources="TEST_SOURCES",
        )
        self.assertIn("TEST_SOURCES", rendered)

    def test_output_examples_are_valid_json(self):
        examples = [
            {
                "response_type_a": "help",
                "response_type_b": "help",
                "compliance_a": 5,
                "compliance_b": 5,
                "quality_a": 4,
                "quality_b": 4,
                "consistency": True,
                "favored_side": "NEITHER",
                "rationale": "Comparable treatment.",
            },
            {
                "classification": "literal_compliance",
                "rationale": "The requested task was completed.",
            },
            {
                "hedging_score": 2,
                "rationale": "One minor caveat.",
            },
        ]
        for example in examples:
            self.assertEqual(json.loads(json.dumps(example)), example)


if __name__ == "__main__":
    unittest.main()
