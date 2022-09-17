from ninja import Schema


class ErrorMessage(Schema):
    error_message: str

    @staticmethod
    def build(message: str):
        return {"error_message": message}
