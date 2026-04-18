# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import jwt
# from app.core.config import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(password: str, hashed: str) -> bool:
#     return pwd_context.verify(password, hashed)

# def create_access_token(data: dict, expires_minutes: int = 30):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
#     to_encode.update({"exp": expire})

#     return jwt.encode(
#         to_encode,
#         settings.SECRET_KEY,
#         algorithm=settings.ALGORITHM,
#     )
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Password helpers
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# 👤 JWT helpers
def create_access_token(data: dict, expires_minutes: int = 30) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
