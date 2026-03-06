from typing import Dict, List, Optional

from src.core.exception import CustomException
from src.core.llm.llm_provider import get_llm
from src.core.logger import logger
from src.memory.session_store import SessionStore
from src.prompts.rewrite_prompt import retriever_prompt


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
                        print(f"This is the last question : {last_question}")
                        break
            prompt = retriever_prompt.format(
                last_question=last_question, new_question=new_question
            )

            messages = [{"role": "user", "content": prompt}]
            print("new question , before rewriting", messages)
            rewritten = self.llm.invoke(messages=messages)

            return rewritten

        except Exception as e:
            logger.info("Query rewriting failed")
            raise CustomException(e)


# if __name__ == "__main__":
#     llm = get_llm(temperature=0.0)
#     rewriter = QueryRewriter()

#     q2 = input("Enter old question:")
#     q1 = input("Enter new question:")

#     q3 = rewriter.rewrite(new_question=q1, chat_history=None)
#     messages = [{"role": "user", "content": prompt}]

#     new_quesiton = llm.invoke(messages=messages)

#     print(type(new_quesiton))
#     print(f"New quesiton : \n{new_quesiton}")
