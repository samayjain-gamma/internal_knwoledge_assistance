# from typing import List

# from src.core.exception import CustomException
# from src.core.logger import logger


# class TextSplitter:

#     def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
#         self.chunk_size = chunk_size
#         self.chunk_overlap = chunk_overlap

#     def split(self, text: str) -> List[str]:
#         """
#         Split text into chunks
#         """
#         try:
#             logger.info("Chunking started")
#             chunks = []
#             start = 0

#             while start < len(text):
#                 end = start + self.chunk_size
#                 chunk = text[start:end]
#                 chunks.append(chunk)

#                 start = end - self.chunk_overlap

#             return chunks

#         except Exception as e:
#             logger.error("Failed to do splitting of text")
#             raise CustomException(e)


import re
from typing import List

from src.core.exception import CustomException
from src.core.logger import logger


class SemanticTextSplitter:

    def __init__(self, chunk_size: int = 800, chunk_overlap_sentences: int = 1):
        self.chunk_size = chunk_size
        self.chunk_overlap_sentences = chunk_overlap_sentences

    def split(self, text: str) -> List[str]:
        try:
            paragraphs = text.split("\n\n")
            chunks = []

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                if len(para) <= self.chunk_size:
                    chunks.append(para)
                else:
                    sentences = self._split_into_sentences(para)
                    chunks.extend(self._merge_sentences(sentences))

            return chunks

        except Exception as e:
            logger.error("Semantic splitting failed")
            raise CustomException(e)

    def _split_into_sentences(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?]) +", text)
        return [s.strip() for s in sentences if s.strip()]

    def _merge_sentences(self, sentences: List[str]) -> List[str]:
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) <= self.chunk_size:
                current_chunk.append(sentence)
                current_length += len(sentence)
            else:
                chunks.append(" ".join(current_chunk))

                overlap = (
                    current_chunk[-self.chunk_overlap_sentences :]
                    if self.chunk_overlap_sentences > 0
                    else []
                )
                current_chunk = overlap + [sentence]
                current_length = sum(len(s) for s in current_chunk)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
