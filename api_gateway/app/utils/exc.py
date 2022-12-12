from fastapi import HTTPException, status

exceptions = {
    "credentials_exc": HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ),
    "expire_exc": HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="JWT token expired",
        headers={"WWW-Authenticate": "Bearer"},
    ),
    "apikey_exc": HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect API Key",
        headers={"WWW-Authenticate": "Bearer"},
    ),
    "inactive_exc": HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Available only for active consumers",
    ),
    "not_found_exc": HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Not Found"
    ),
}
