from typing import Dict, List

import ollama

from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.llm.llm_provider import get_llm
from src.core.logger import logger
from src.prompts.rag_prompts import build_grounded_rag_prompt

variables = get_settings()


class Generator:
    """ """

    def __init__(self):
        self.llm = get_llm()

    def generate(self, query: str, contexts: List[Dict]) -> str:
        try:
            logger.info("generation part activated")
            prompt = build_grounded_rag_prompt(query, contexts)

            messages = [{"role": "user", "content": prompt}]

            print("\nAnswer:\n")
            print("-" * 60)

            full_response = ""

            for token in self.llm.stream(messages):
                print(token, end="", flush=True)
                full_response += token

            print("\n" + "-" * 60)

            logger.info(
                {
                    "event": "generation_success",
                    "query": query,
                }
            )

            return full_response

        except Exception as e:
            logger.error("Generation failed")
            raise CustomException(e)
