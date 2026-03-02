from typing import Dict, List

import ollama

from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.logger import logger
from src.prompts.rag_prompts import build_grounded_rag_prompt

variables = get_settings()


class Generator:
    """ """

    def __init__(self, model_name: str = variables.LLM_MODEL):
        self.model_name = model_name

    def generate(self, query: str, contexts: List[Dict]) -> str:
        try:
            logger.info("generation part activated")
            prompt = build_grounded_rag_prompt(query, contexts)

            stream = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )

            full_response = ""

            print("\nAnswer:\n")
            print("-" * 60)

            for chunk in stream:
                token = chunk["message"]["content"]
                print(token, end="", flush=True)
                full_response += token

            print("\n" + "-" * 60)

            logger.info(
                {
                    "event": "generation_success",
                    "query": query,
                }
            )

            logger.info("generation part ended")
            return full_response

        except Exception as e:
            logger.error("Generation failed")
            raise CustomException(e)

    # OLLAMA_BASE_URL: str = "http://localhost:11434"
    # LLM_MODEL: str = "phi3"
    # LLM_TEMPERATURE: float = 0.2
    # LLM_MAX_TOKENS: int = 512
