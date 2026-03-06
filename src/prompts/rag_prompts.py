from typing import Dict, List


def build_grounded_rag_prompt(query: str, contexts: List[Dict]) -> str:

    context_block = ""

    for chunk in contexts:
        context_block += chunk["content"] + "\n\n"

    prompt = f"""
You are an internal company assistant.

STRICT RULES:

 Answer ONLY using the provided context.
 Do NOT use outside knowledge.
 If the answer is not present in the context, respond with:
  "I could not find this information in the company documents."
 Do NOT include citations.
 Keep the answer concise (2-4 sentences maximum).

CONTEXT:
{context_block}

QUESTION:
{query}

INSTRUCTIONS:
Provide a clear and short answer based only on the context.
"""
    return prompt.strip()
