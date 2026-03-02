from pathlib import Path
from typing import List

from src.core.exception import CustomException
from src.core.logger import logger


class DocumentLoader:

    @staticmethod
    def load_text_file(file_path: str) -> str:
        """
        loads file from disk to in memory for chunking
        """
        try:
            return Path(file_path).read_text()
        except Exception as e:
            logger.error("Failed to load file")
            raise CustomException(e)

    @staticmethod
    def load_directory(directory_path: str) -> List[str]:
        """
        loads whole diretory data from directory to in memory for chunking
        """
        try:
            texts = []
            for path in Path(directory_path).rglob("*.txt"):  # rglob - recursive glob
                texts.append(path.read_text(encoding="utf-8"))
            return texts
        except Exception as e:
            logger.error("Failed to load directory")
            raise CustomException(e)
