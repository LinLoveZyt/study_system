# app/prompts/profile_prompts.py
SYSTEM_PROMPT = """
You are a top-tier cognitive psychology expert and educational planner. Your task is to analyze a learner's self-assessment questionnaire and generate a structured JSON report of their learner profile.
You MUST respond with a valid JSON object, and nothing else. Do not include any explanatory text before or after the JSON.
"""

def get_profile_generation_prompt(assessment_data: dict) -> str:
    return f"""
    Please analyze the following questionnaire data and generate the learner profile JSON.

    Questionnaire Data:
    ```json
    {assessment_data}
    ```

    Strictly adhere to the following JSON format. Do not add any comments or extra fields.
    The values for "motivation_type", "self_assessed_confidence", "vark_primary", "social_preference", "structure_preference", and "metacognition_level" must be chosen from the provided options.

    JSON Format to follow:
    {{
      "profile_summary": "A concise paragraph summarizing the learner's core traits, strengths, and potential challenges.",
      "learning_goals": {{
        "primary_goal": "The main learning goal.",
        "motivation_type": "intrinsic / extrinsic / mixed",
        "potential_barriers": ["List of potential barriers."]
      }},
      "baseline_assessment": {{
        "self_assessed_confidence": "high / medium / low",
        "common_difficulties": ["List of common difficulties in learning."]
      }},
      "learning_style": {{
        "vark_primary": "visual / auditory / read-write / kinesthetic",
        "vark_secondary": "visual / auditory / read-write / kinesthetic / none",
        "social_preference": "independent / collaborative",
        "structure_preference": "structured / exploratory"
      }},
      "cognitive_profile": {{
        "metacognition_level": "high / medium / low",
        "notes": "Other noteworthy cognitive characteristics."
      }}
    }}
    """

