from fastapi import HTTPException, status


UNAUTHORIZED = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

USERALREADYEXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with this email already exists.",
)