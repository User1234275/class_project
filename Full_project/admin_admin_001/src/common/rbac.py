from fastapi import Header, HTTPException, status
import os

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "super-secret-admin-key")

def admin_required(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    # In a real app, fetch admin_id from DB or token
    return {"admin_id": 1}
