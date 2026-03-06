import re
from typing import Dict

from src.core.logger import logger
from src.guardrails.injection_detector import InjectionDetector
from src.guardrails.input_validator import InputValidator
from src.memory.query_rewriter import QueryRewriter
from src.memory.session_store import SessionStore
from src.rag.generator import Generator
from src.rag.retriever import Retriever

# from src.core.exception import CustomException


input_validator = InputValidator()
query_rewriter = QueryRewriter()
retriever = Retriever()
generator = Generator()
injection_detector = InjectionDetector()
memory = SessionStore()


def get_user_input(state):
    user_input = input("User:")
    user_input = user_input.strip().lower()
    return {"user_input": user_input}


def check_exit(state):
    print("Entered into check_exit  router")
    text = state["user_input"]

    if text == "exit":
        print("User entered 'exit', exiting from chat")
        return {"exit": True}

    print("Exiting from check_exit check")
    return {"exit": False, "query": text}


def exit_router(state):
    return state["exit"]


def validate_input(state: Dict):
    print("Entered into validate_input router")
    query = state["query"]
    print("query in validate input router : ", query)
    is_valid = input_validator.validate(query=query)
    print("query is valid or not : ", is_valid)
    return {"input_validation_flag": is_valid}


def input_validation_check(state):
    print("Enterd into input validation check router")
    return state["input_validation_flag"]


def detect_injection(state):
    logger.info("running injection detection")
    query = state["query"]

    flag = injection_detector.detect(query=query)
    return {"injection_flag": flag}


def detect_injection_check(state):
    print("Entered in to detect injection router check")
    if state["injection_flag"]:
        print("User entered change configuratin prompt")
    return state["injection_flag"]


def rewrite_query(state):

    print("rewrite_query")
    query = state["query"]
    history = state.get("history", [])

    if history:
        rewritten = query_rewriter.rewrite(chat_history=history, new_question=query)
    else:
        rewritten = query
    print(f"New querry :\n{rewritten}")
    return {"rewritten_query": rewritten}


def retrieve_docs(state):
    print("retrieving documents")
    query = state["rewritten_query"]
    docs = retriever.retrieve(query)

    return {"retrieved_docs": docs}


def generate_answer(state: Dict):

    query = state["rewritten_query"]
    docs = state["retrieved_docs"]

    answer = generator.generate(query=query, contexts=docs)

    return {"generated_answer": answer}


def update_history(state):

    history = state.get("history", [])

    history.append({"role": "user", "content": state["rewritten_query"]})

    history.append({"role": "assistant", "content": state["generated_answer"]})

    return {"history": history}
