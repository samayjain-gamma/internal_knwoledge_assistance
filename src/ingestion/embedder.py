from typing import List

import ollama

from src.core.exception import CustomException
from src.core.logger import logger


class Embedder:

    def __init__(self, model_name: str = "nomic-embed-text"):
        self.model_name = model_name

    def embed(self, texts: List[str]) -> List[List[float]]:
        try:
            logger.info("embedding started")
            embeddings = []

            # below method is bad when embeddng 100s of files
            for text in texts:
                response = ollama.embeddings(model=self.model_name, prompt=text)
                embeddings.append(response["embedding"])

            logger.info("Embedding completed")
            return embeddings

        except Exception as e:
            logger.error("failed to do embedding")
            raise CustomException(e)
