from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "dfb34n4jfn93hf9834hf93hf9834h9fh394hf98h3f9h3f9h34f9h3f9h34f9h3f9h3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain: str, stored: str):
    """Simple plain text password check (no hashing)"""
    return plain == stored


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Generate a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    """Decode a JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
