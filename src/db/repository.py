from typing import Any, Dict, List

from src.core.exception import CustomException
from src.core.logger import logger
from src.db.chroma_client import ChromaClientManager


class VectorRepository:
    """
    Abstracts all vector database operations.
    """

    def __init__(self):
        try:
            self.collection = ChromaClientManager().get_collection()
        except Exception as e:
            raise CustomException("VectorRepository initialization failed", e)

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
    ):
        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            logger.info(
                {
                    "event": "documents_added",
                    "count": len(ids),
                }
            )

        except Exception as e:
            raise CustomException(e)

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 4,
        where: Dict[str, Any] = None,
    ):
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
            )

            logger.info(
                {
                    "event": "vector_query",
                    "top_k": top_k,
                }
            )

            return results

        except Exception as e:
            raise CustomException(e)

    def count(self) -> int:
        try:
            return self.collection.count()
        except Exception as e:
            raise CustomException(e)

    def delete_collection(self):
        try:
            self.collection.delete()
            logger.warning({"event": "collection_deleted"})
        except Exception as e:
            raise CustomException(e)
