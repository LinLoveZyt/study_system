# app/services/task_manager.py
import json
import uuid
from ..core import config, llm_client
from ..prompts import task_prompts
from . import profile_manager, pdf_generator
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_all_tasks():
    tasks = []
    for task_dir in config.LEARNING_MATERIALS_DIR.iterdir():
        if task_dir.is_dir():
            metadata_path = task_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    tasks.append(json.load(f))
    # Sort tasks by creation date, newest first
    tasks.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return tasks

def create_learning_task(task_request: dict):
    user_profile = profile_manager.get_profile()
    if not user_profile:
        raise ValueError("User profile not found. Cannot create a task.")

    logger.info(f"Generating learning material for task: {task_request.get('topic')}")
    prompt = task_prompts.get_task_generation_prompt(task_request, user_profile)
    system_prompt = task_prompts.SYSTEM_PROMPT
    
    learning_material_json = llm_client.generate_json(prompt, system_prompt)
    
    if not learning_material_json:
        logger.error("Failed to generate learning material JSON from LLM.")
        return None

    logger.info("Successfully generated learning material JSON.")
    
    task_id = str(uuid.uuid4())
    task_dir = config.LEARNING_MATERIALS_DIR / task_id
    task_dir.mkdir(exist_ok=True)
    
    json_path = task_dir / "learning_material.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(learning_material_json, f, indent=4, ensure_ascii=False)
        
    logger.info(f"Learning material JSON saved to {json_path}")

    # Generate PDF
    pdf_filename = "learning_material.pdf"
    pdf_path = task_dir / pdf_filename
    pdf_generator.generate_pdf_from_json(learning_material_json, pdf_path)
    
    # Save metadata
    metadata = {
        "task_id": task_id,
        "topic": task_request.get("topic"),
        "title": learning_material_json.get("title", "Untitled Task"),
        "created_at": datetime.now().isoformat(),
        "pdf_url": f"/materials/{task_id}/{pdf_filename}"
    }
    metadata_path = task_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
        
    logger.info(f"Task metadata saved to {metadata_path}")
    
    return metadata
