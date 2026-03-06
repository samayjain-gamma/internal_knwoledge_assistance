from src.core.config import get_settings
from src.core.exception import CustomException
from src.core.logger import logger
from src.memory.query_rewriter import QueryRewriter
from src.memory.session_store import SessionStore
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


# if __name__ == "__main__":
#     rag = RAGPipeline()

#     while True:
#         question = input("\nAsk question (or type 'exit' to exit): ")

#         if question == "exit":
#             break

#         rag.ask(question)


class ConversationalRAG:

    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()
        self.memory = SessionStore()
        self.rewriter = QueryRewriter()

    def ask(self, question: str) -> str:
        if self.memory.get_history():
            standalone_query = self.rewriter.rewrite(
                self.memory.get_history(), question
            )
        else:
            standalone_query = question

        print(f"\nStandalone Query: {standalone_query}\n")

        contexts = self.retriever.retrieve(standalone_query)

        answer = self.generator.generate(standalone_query, contexts)

        self.memory.add_user_message(question)
        self.memory.add_assistant_message(answer)

        return answer


if __name__ == "__main__":
    try:
        rag = ConversationalRAG()
        logger.info("Entered into Conversational Rag system")
        while True:
            q = input("\nAsk (or type 'exit'): ")

            if q.lower() == "exit":
                break

            rag.ask(q)

    except Exception as e:
        logger.error("Conversational RAG pipeline is not working")
        raise CustomException(e)
