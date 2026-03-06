from src.core.exception import CustomException
from src.core.logger import logger


class InputValidator:
    """
    Validates raw input before processing.
    """

    def __init__(self):
        self.MIN_LENGTH = 4
        self.MAX_LENGTH = 50

    def validate(self, query: str) -> bool:
        if not isinstance(query, str):
            print(("Input must be a string"))
            return False

        query = query.strip()

        if not query:
            print("Input cannot be empty")
            return False

        if len(query) < self.MIN_LENGTH:
            print(f"Input too short. Minimum length is {self.MIN_LENGTH} characters.")
            return False

        if len(query) > self.MAX_LENGTH:
            print(f"Input too long. Maximum length is {self.MAX_LENGTH} characters.")
            return False
        return True


if __name__ == "__main__":
    validator = InputValidator()

    test_cases = [
        "",
        "Hi",
        "What is leave policy?",
        "A" * 1200,
        123,
    ]
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {repr(test)}")

        try:
            result = validator.validate(test)
            print("VALID:", result)
        except Exception as e:
            print("ERROR:", e)
