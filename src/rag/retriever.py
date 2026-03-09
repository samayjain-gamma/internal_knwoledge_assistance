import time
from typing import Any, Dict, List

from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.logger import logger
from src.db.repository import VectorRepository
from src.ingestion.embedder import Embedder
from src.monitoring.metrics import RETRIEVER_LATENCY

variables = get_settings()


class Retriever:
    """
    Handles user querry
    Sememtic retrieval
    """

    def __init__(self, top_k=variables.RETRIEVAL_TOP_K):
        try:
            self.top_k = top_k
            self.embedder = Embedder()
            self.repo = VectorRepository()

        except Exception as e:
            logger.error("Retriever initialization failed")
            raise CustomException(e)

    def retrieve(self, querry: str) -> List[Dict[str, Any]]:
        try:
            start = time.time()

            querry_embedded = self.embedder.embed([querry])[0]

            results = self.repo.query(query_embedding=querry_embedded, top_k=self.top_k)

            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            formatted_results = []

            for doc, meta, dist in zip(documents, metadatas, distances):
                formatted_results.append(
                    {
                        "content": doc,
                        "metadata": meta,
                        # "score": dist,
                    }
                )
            logger.info(
                {
                    "event": "retrieval_success",
                    "query": querry,
                    "results_count": len(formatted_results),
                }
            )

            RETRIEVER_LATENCY.observe(time.time() - start)
            return formatted_results

        except Exception as e:
            logger.error("Retrieval failed")
            raise CustomException(e)


if __name__ == "__main__":

    retriever = Retriever()

    while True:
        query = input("\nEnter query (or type 'exit'): ")

        if query.lower() == "exit":
            break

        results = retriever.retrieve(query)

        print("\nTop Results:\n")

        for i, r in enumerate(results, 1):
            print(f"Result {i}")
            print("-" * 40)
            # print("Score:", r["score"])
            print("Source:", r["metadata"])
            print("Content:\n", r["content"])
            print("\n\n\n")
