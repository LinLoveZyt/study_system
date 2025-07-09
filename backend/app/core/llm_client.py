import ollama
import json
import logging
import re
from typing import Optional, Dict, Any
from . import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        logger.info("Initializing LLM client...")
        self.retry_attempts = config.LLM_JSON_RETRY_ATTEMPTS
        self.client = ollama.Client(timeout=config.OLLAMA_TIMEOUT)
        
        try:
            logger.info(f"Checking for LLM model '{config.OLLAMA_MODEL_NAME}'...")
            self.client.show(config.OLLAMA_MODEL_NAME)
            logger.info(f"✅ LLM model '{config.OLLAMA_MODEL_NAME}' is available.")
            self._initialized = True
        except Exception as e:
            logger.error(f"❌ LLM model initialization failed: {e}")
            logger.error(f"Please ensure the Ollama service is running and the model '{config.OLLAMA_MODEL_NAME}' has been downloaded.")
            raise ConnectionError(f"Cannot connect to Ollama model '{config.OLLAMA_MODEL_NAME}'")

    def generate_json(self, prompt: str, system_prompt: str) -> Optional[Dict[str, Any]]:
        for attempt in range(self.retry_attempts):
            logger.info(f"Attempting to generate JSON (attempt {attempt + 1}/{self.retry_attempts})...")
            try:
                 response = self.client.chat(
                    model=config.OLLAMA_MODEL_NAME,
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': prompt}
                    ],
                    format='json', # 使用 Ollama 的 JSON 模式
                    options={'temperature': 0.2}
                )
                 raw_response = response['message']['content']
            except Exception as e:
                logger.error(f"LLM call failed during JSON generation: {e}")
                continue

            try:
                # Ollama 在 format='json' 模式下会直接返回合法的 JSON 字符串
                parsed_json = json.loads(raw_response)
                logger.info("Successfully parsed JSON from LLM response.")
                return parsed_json
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON: {e}. LLM raw response:\n---\n{raw_response}\n---")
                if attempt >= self.retry_attempts - 1:
                    logger.error("Max retry attempts reached, failed to get valid JSON.")
                    return None
        return None

# 单例模式的客户端实例
llm_client = LLMClient()