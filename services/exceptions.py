class CustomError(Exception):
    def __init__(self, code: int, message: str, error: str):
        self.res = {
            "code": code,
            "message": message,
            "error": error,
        }
        super().__init__(self.res)


class StTConnectionError(CustomError):
    def __init__(self, error: str):
        super().__init__(
            code=1000,
            message="Connection to Google Speech to Text API Failed.",
            error=error,
        )


class StTOperationError(CustomError):
    def __init__(self, error: str):
        super().__init__(
            code=1001,
            message="Getting text from Google Speech to Text Failed.",
            error=error,
        )


class OpenAIError(CustomError):
    def __init__(self, error: str):
        super().__init__(
            code=1002,
            message="GPT failed.",
            error=error,
        )


class TranslationError(CustomError):
    def __init__(self, error: str):
        super().__init__(
            code=1003,
            message="Translator failed.",
            error=error,
        )


class StorageError(CustomError):
    def __init__(self, error: str):
        super().__init__(
            code=1004,
            message="Uploading file to cloud storage failed.",
            error=error,
        )
