from chromadb import PersistentClient
from chromadb.config import Settings as ChromaSettings

from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.logger import logger


class ChromaClientManager:
    """
    Manages persistent Chroma client and collection.
    """

    def __init__(self):
        try:
            settings = get_settings()

            self.persist_dir = str(settings.CHROMA_PERSIST_DIR)
            self.collection_name = settings.CHROMA_COLLECTION_NAME

            self.client = PersistentClient(
                path=self.persist_dir,
                settings=ChromaSettings(anonymized_telemetry=False),
            )

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )

            logger.info(
                {
                    "event": "chroma_initialized",
                    "collection": self.collection_name,
                    "persist_dir": self.persist_dir,
                }
            )

        except Exception as e:
            logger.error("Failed to initialize Chrome client")
            raise CustomException("Failed to initialize Chroma client", e)

    def get_collection(self):
        return self.collection
