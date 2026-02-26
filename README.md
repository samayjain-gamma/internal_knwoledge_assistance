Capstone — Build It End-to-End (Week 9–10)
The Project
Build a complete, production-ready AI application. This is where everything comes together.
System: Internal Knowledge Assistant
Build a system where employees can ask questions about company documents and get accurate, sourced answers.
Requirements:

Document ingestion pipeline: upload PDFs/docs → extract text → chunk → embed → store in vector DB
RAG-powered Q&A: user asks a question → retrieve relevant chunks → generate grounded answer with citations
Conversation memory: follow-up questions should use context from previous turns
Streaming responses: token-by-token streaming to the frontend
Guardrails: input validation, prompt injection detection, output grounding checks, PII filtering
RBAC: users only see answers from documents they have access to
Evaluation: automated test suite with 50+ test questions, measuring retrieval accuracy, answer quality, and hallucination rate
Monitoring: request logging, latency tracking, cost tracking, error alerting
API design: versioned, documented, rate-limited, with health checks

Evaluation criteria:

Does it answer correctly when it should?
Does it say "I don't know" when it should?
Does it resist prompt injection?
Does it handle errors gracefully?
Can you explain every design decision you made?

-----------------------------------------------