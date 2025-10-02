from fastapi import HTTPException, status

def not_found(detail: str = "Not found"):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

def conflict(detail: str = "Conflict"):
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
