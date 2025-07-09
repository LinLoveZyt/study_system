# app/prompts/task_prompts.py
import json

SYSTEM_PROMPT = """
You are an experienced instructional designer and a subject matter expert in the user's requested field.
Your task is to create a personalized learning material in a structured JSON format based on the learner's profile and their task request.
You MUST respond with a valid JSON object, and nothing else. Do not add any explanatory text before or after the JSON.
"""

def get_task_generation_prompt(task_request: dict, user_profile: dict) -> str:
    return f"""
    # Learner Profile (Context)
    ```json
    {json.dumps(user_profile, indent=2)}
    ```

    # Learning Task Request (Instruction)
    ```json
    {json.dumps(task_request, indent=2)}
    ```

    # Your Task
    Based on the **Learner Profile** and **Learning Task Request**, generate a structured JSON for the learning material.

    ## Personalization Guidelines:
    - **Content Depth**: Adjust the complexity based on the learner's `knowledge_level`.
    - **Learning Style**: Tailor the `explanation` and `visual_analogy` to the learner's `vark_primary` style. For example, use metaphors for 'visual' learners, and step-by-step logic for 'read-write' learners.
    - **Structure**: If the learner prefers `structured` guidance, ensure the sections flow logically from simple to complex.
    - **Metacognition**: Use the `reflection_prompt` to encourage self-assessment, especially if their `metacognition_level` is not high.

    ## JSON Output Format
    Strictly follow this JSON structure. Ensure all fields are filled appropriately.
    {{
      "title": "A suitable title for the learning module.",
      "learning_objectives": [
        "After completing this module, the learner will be able to...",
        "Objective 2...",
        "Objective 3..."
      ],
      "content_sections": [
        {{
          "section_title": "Title of the first knowledge point",
          "explanation": "A detailed explanation tailored to the user's learning style. Use clear, simple language.",
          "code_example": "Provide a clear, runnable code example if applicable. Otherwise, provide a concrete example.",
          "visual_analogy": "A metaphor or analogy to help a visual learner. If not applicable, provide a real-world scenario.",
          "reflection_prompt": "An insightful question to prompt the learner to reflect on the concept."
        }}
      ],
      "practice_exercises": [
        {{
          "question_type": "multiple_choice",
          "question_text": "A multiple-choice question to test understanding.",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "answer": "The correct option, e.g., 'Option C'",
          "feedback": "A brief explanation of why the answer is correct."
        }},
        {{
          "question_type": "coding_challenge",
          "question_text": "A practical coding problem or a short-answer question.",
          "expected_output": "The expected result or a model answer."
        }}
      ]
    }}
    """