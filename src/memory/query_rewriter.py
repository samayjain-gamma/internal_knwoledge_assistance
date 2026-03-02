from typing import Dict, List

from src.core.exception import CustomException
from src.core.llm.llm_provider import get_llm
from src.core.logger import logger
from src.prompts.rewrite_prompt import build_rewrite_prompt


class QueryRewriter:

    def __init__(self):
        self.llm = get_llm(temperature=0.0)

    def rewrite(self, chat_history: List[Dict[str, str]], new_question: str) -> str:

        try:
            logger.info("Prompt reqritting")
            prompt = build_rewrite_prompt(
                new_question=new_question,
                chat_history=chat_history,
            )

            messages = [{"role": "user", "content": prompt}]
            rewritten = self.llm.invoke(messages=messages)

            return rewritten.strip()

        except Exception as e:
            logger.info("Prompt rewriting failed")
            raise CustomException(e)
