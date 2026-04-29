from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException,Cookie
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
SECRET_KEY = os.getenv("SEC_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# -------------------------------
# JWT creation function
# -------------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------------------
# JWT verification function
# -------------------------------
from fastapi import Header

def verify_jwt(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 🔥 IMPORTANT: check expiry manually safety (optional but good)
        if payload.get("exp") and datetime.utcnow().timestamp() > payload["exp"]:
            raise HTTPException(status_code=401, detail="Token expired")

        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")