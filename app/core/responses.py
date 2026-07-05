from typing import Any

from fastapi.responses import ORJSONResponse


class SuccessResponse(ORJSONResponse):
    def __init__(
        self,
        data: Any = None,
        message: str = "Success",
        status_code: int = 200,
    ):
        super().__init__(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data,
            },
        )


class ErrorResponse(ORJSONResponse):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        errors: Any = None,
    ):
        super().__init__(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "errors": errors,
            },
        )