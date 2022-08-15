from passlib.context import CryptContext

pwd_contect = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash Password

def hash(password: str):
    return pwd_contect.hash(password)

# Verify Hash Password

def verify(plain_pass, hashed_pass):
    return pwd_contect.verify(plain_pass, hashed_pass)