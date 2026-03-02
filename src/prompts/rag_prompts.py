from typing import Dict, List


def build_grounded_rag_prompt(query: str, contexts: List[Dict]) -> str:
    """
    Builds a strictly grounded RAG prompt.
    """

    context_block = ""

    for i, chunk in enumerate(contexts, 1):
        context_block += f"[Source {i}]\n"
        context_block += chunk["content"] + "\n\n"

    prompt = f"""
You are an internal company assistant.

STRICT RULES:
- Answer ONLY using the provided context.
- Do NOT use outside knowledge.
- If the answer is not present, say:
  "I could not find this information in the company documents."

CONTEXT:
{context_block}

QUESTION:
{query}

INSTRUCTIONS:
- Provide a clear and structured answer.
- At the end, include citations like:
  (Source 1), (Source 2)
"""

    return prompt.strip()
