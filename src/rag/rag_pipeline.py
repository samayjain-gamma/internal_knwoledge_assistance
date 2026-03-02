from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.logger import logger
from src.rag.generator import Generator
from src.rag.retriever import Retriever

variables = get_settings()


class RAGPipeline:
    """
    This is the RAG pipeline
    """

    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def ask(self, query: str) -> str:
        contexts = self.retriever.retrieve(query)
        answer = self.generator.generate(query, contexts)
        return answer


if __name__ == "__main__":
    rag = RAGPipeline()

    while True:
        question = input("\nAsk question (or type 'exit' to exit): ")

        if question == "exit":
            break

        rag.ask(question)
