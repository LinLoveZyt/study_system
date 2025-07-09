import json
from ..core import config, llm_client
from ..prompts import profile_prompts
import logging

logger = logging.getLogger(__name__)
USER_ID = "default_user" # Hardcoded for this DEMO

def get_user_profile_path():
    return config.USER_PROFILES_DIR / f"{USER_ID}_profile.json"

def check_profile_exists():
    return get_user_profile_path().exists()

def get_profile():
    if not check_profile_exists():
        return None
    with open(get_user_profile_path(), 'r', encoding='utf-8') as f:
        return json.load(f)

def create_profile(assessment_data: dict):
    logger.info("Generating user profile from assessment data...")
    prompt = profile_prompts.get_profile_generation_prompt(assessment_data)
    system_prompt = profile_prompts.SYSTEM_PROMPT
    
    profile_json = llm_client.generate_json(prompt, system_prompt)
    
    if profile_json:
        logger.info("Successfully generated profile JSON from LLM.")
        with open(get_user_profile_path(), 'w', encoding='utf-8') as f:
            json.dump(profile_json, f, indent=4, ensure_ascii=False)
        logger.info(f"User profile saved to {get_user_profile_path()}")
        return profile_json
    else:
        logger.error("Failed to generate profile JSON from LLM.")
        return None
