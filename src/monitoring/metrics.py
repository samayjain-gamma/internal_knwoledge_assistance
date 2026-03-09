from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter("rag_request_total", "Total number of RAG requests")

RAG_LATENCY = Histogram("rag_pipeline_latency_seconds", "End to end RAG latency")


LLM_GENERATING_LATENCY = Histogram(
    "llm_latency_seconds", "Time spent generating LLM response"
)


QUERY_REWRITE_LATENCY = Histogram(
    "query_rewrite_latency_seconds", "Query rewrite latency seconds"
)

RETRIEVER_LATENCY = Histogram(
    "retriever_latency_seconds", "Time spend in gathering all documents"
)


LLM_REQUESTS = Counter("llm_requests_total", "Total number of LLM calls")

PROMPT_TOKENS = Counter("llm_prompt_tokens_total", "Total prompt tokens used")

COMPLETION_TOKENS = Counter(
    "llm_completion_tokens_total", "Total completion tokens generated"
)

TOTAL_TOKENS = Counter("llm_total_tokens_total", "Total tokens consumed")


def start_metrics_server():
    start_http_server(8001)
