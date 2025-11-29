from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "dfb34n4jfn93hf9834hf93hf9834h9fh394hf98h3f9h3f9h34f9h3f9h34f9h3f9h3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password, stored_password):
    """Simple text comparison (no hashing)"""
    return plain_password == stored_password

def create_access_token(data: dict):
    """Generate JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
