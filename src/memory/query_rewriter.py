from typing import Dict, List, Optional

from src.core.exception import CustomException
from src.core.llm.llm_provider import get_llm
from src.core.logger import logger
from src.memory.session_store import SessionStore
from src.prompts.rewrite_prompt import build_rewrite_prompt


class QueryRewriter:

    def __init__(self):
        self.llm = get_llm()

    def rewrite(
        self, chat_history: Optional[List[Dict[str, str]]], new_question: str
    ) -> str:

        try:
            logger.info("Prompt reqritting")
            last_question = None
            if chat_history:
                for msg in reversed(chat_history):
                    if msg.get("role") == "user":
                        last_question = msg.get("content")
                        break

            prompt = build_rewrite_prompt(
                new_question=new_question,
                last_question=last_question,
            )

            messages = [{"role": "user", "content": prompt}]
            print("new queestion , before rewriting", messages)
            rewritten = self.llm.invoke(messages=messages)

            return rewritten.strip()

        except Exception as e:
            logger.info("Query rewriting failed")
            raise CustomException(e)


if __name__ == "__main__":
    llm = get_llm(temperature=0.0)

    q2 = input("Enter old question")
    q1 = input("Enter new question")

    prompt = build_rewrite_prompt(last_question=q2, new_question=q1)
    messages = [{"role": "user", "content": prompt}]
    new_quesiton = llm.invoke(messages=messages)

    print(type(new_quesiton))
    print(f"New quesiton : \n{new_quesiton}")
