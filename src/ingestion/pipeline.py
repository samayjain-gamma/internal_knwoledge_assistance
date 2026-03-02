import uuid
from typing import List

from src.core.exception import CustomException
from src.core.logger import logger
from src.db.repository import VectorRepository
from src.ingestion.embedder import Embedder
from src.ingestion.loader import DocumentLoader
from src.ingestion.splitter import TextSplitter


class IngestionPipeline:

    def __init__(self):
        self.loader = DocumentLoader()
        self.splitter = TextSplitter()
        self.embedder = Embedder()
        self.repo = VectorRepository()

    def ingest_file(self, file_path: str):

        try:

            logger.info(f"data ingestion pipeline started for file {file_path}")

            raw_text = self.loader.load_text_file(file_path)

            chunks = self.splitter.split(raw_text)

            embeddings = self.embedder.embed(chunks)

            ids = [str(uuid.uuid4()) for _ in chunks]
            metadatas = [{"source": file_path} for _ in chunks]

            self.repo.add_documents(
                ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas
            )

            logger.info("data ingestion pipeline added")
            return len(chunks)

        except Exception as e:
            logger.error("Error occured in data ingestion pipeline")
            raise CustomException(e)
