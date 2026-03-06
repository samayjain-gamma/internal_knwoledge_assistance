from typing import Dict, List


def build_rewrite_prompt(new_question: str, last_question: str) -> str:

    prompt = """ Previous user question:
{last_question}

Current user question:
{new_question}

Task:
If the current question depends on the previous question for context, rewrite it so that it becomes a complete standalone question.

If the current question is already independent or unrelated, return it unchanged.

Output rules:
- Return ONLY the rewritten question.
- Do NOT add explanation or additional text."""
    return prompt.strip()
