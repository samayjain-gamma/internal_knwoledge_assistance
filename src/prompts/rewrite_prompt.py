from typing import Dict, List


def build_rewrite_prompt(chat_history: List[Dict[str, str]], new_question: str) -> str:
    """
    Builds prompt to convert follow-up question
    into standalone question.
    """

    history_block = ""

    for msg in chat_history:
        role = msg["role"].capitalize()
        history_block += f"{role}: {msg['content']}\n"

    prompt = f"""
You are a query rewriting assistant.

Your task:
Rewrite the follow-up question into a fully standalone question
that can be understood without conversation history.

Do NOT answer the question.
Only rewrite it.

Conversation:
{history_block}

Follow-up Question:
{new_question}

Standalone Question:
"""

    return prompt.strip()
