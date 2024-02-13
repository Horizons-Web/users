from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=404, detail=detail)


class EmailSendError(HTTPException):
    def __init__(self, detail: str = "Error sending email"):
        super().__init__(status_code=500, detail=detail)


class UpdateError(HTTPException):
    def __init__(self, detail: str = "Error updating"):
        super().__init__(status_code=500, detail=detail)


class DecodeError(HTTPException):
    def __init__(self, detail: str = "Error decoding token"):
        super().__init__(status_code=500, detail=detail)


class InvalidCredentials(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=403, detail=detail)


class TokenNotFound(HTTPException):
    def __init__(self, detail: str = "Token not found"):
        super().__init__(status_code=404, detail=detail)


class TokenExpired(HTTPException):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(status_code=403, detail=detail)


class TokenNotActive(HTTPException):
    def __init__(self, detail: str = "Token not active"):
        super().__init__(status_code=403, detail=detail)


class PermissionDenied(HTTPException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=403, detail=detail)


class JWTError(HTTPException):
    def __init__(self, detail: str = "Error decoding token"):
        super().__init__(status_code=400, detail=detail)


class UserNotActive(HTTPException):
    def __init__(self, detail: str = "User not active"):
        super().__init__(status_code=403, detail=detail)
