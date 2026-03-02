from typing import Any, Dict, Generator, List

import ollama

from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.logger import logger

variables = get_settings()


class OllamaLLM:
    """
    Centralized LLM wrapper for Ollama
    """

    def __init__(self, model_name: str, temperature: float):
        self.model_name = model_name
        self.temperature = temperature

    def stream(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """
        Strean Model Output token by token
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                stream=True,
                options={"temperature": self.temperature},
            )

            for chunk in response:
                yield chunk["message"]["content"]

        except Exception as e:
            logger.error("LLM streaming failed.")
            raise CustomException(e)

    def invoke(self, messages: List[Dict[str, str]]) -> str:
        """
        Non streaming call
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                stream=False,
                options={
                    "temperature": self.temperature,
                },
            )

            return response["message"]["content"]

        except Exception as e:
            logger.error("LLM invocation failed")
            raise CustomException(e)


def get_llm(model_name: str = None, temperature: float = None) -> OllamaLLM:
    """
    Return configured LLM instance
    """
    model_name = model_name or variables.LLM_MODEL
    temperature = temperature if temperature is not None else variables.LLM_TEMPERATURE

    return OllamaLLM(model_name=model_name, temperature=temperature)
