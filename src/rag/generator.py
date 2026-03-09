import time
from typing import Dict, List

import ollama

from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.llm.llm_provider import get_llm
from src.core.logger import logger
from src.core.tokenizer import count_tokens
from src.monitoring.metrics import (
    COMPLETION_TOKENS,
    LLM_GENERATING_LATENCY,
    LLM_REQUESTS,
    PROMPT_TOKENS,
    TOTAL_TOKENS,
)
from src.prompts.answer_prompt import answer_prompt

variables = get_settings()


class Generator:

    def __init__(self):
        self.llm = get_llm()

    def generate(self, query: str, contexts: List[Dict]) -> str:
        try:
            start = time.time()

            logger.info("generation part activated")
            prompt = answer_prompt.format(query=query, context_block=contexts)

            messages = [{"role": "user", "content": prompt}]

            prompt_tokens = count_tokens(prompt)
            print("\nAnswer:\n")
            print("-" * 60)

            full_response = ""

            for token in self.llm.stream(messages):
                print(token, end="", flush=True)
                full_response += token

            print("\n" + "-" * 60)

            completion_tokens = count_tokens(full_response)
            total_tokens = prompt_tokens + completion_tokens

            LLM_REQUESTS.inc()
            PROMPT_TOKENS.inc(prompt_tokens)
            COMPLETION_TOKENS.inc(completion_tokens)
            TOTAL_TOKENS.inc(total_tokens)

            logger.info(
                {
                    "event": "generation_success",
                    "query": query,
                }
            )
            LLM_GENERATING_LATENCY.observe(time.time() - start)

            return full_response

        except Exception as e:
            logger.error("Generation failed")
            raise CustomException(e)
