from typing import List

from src.core.exception import CustomException
from src.core.logger import logger


class TextSplitter:

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        """
        Split text into chunks
        """
        try:
            logger.info("Chunking started")
            chunks = []
            start = 0

            while start < len(text):
                end = start + self.chunk_size
                chunk = text[start:end]
                chunks.append(chunk)

                start = end - self.chunk_overlap

            return chunks

        except Exception as e:
            logger.error("Failed to do splitting of text")
            raise CustomException(e)
