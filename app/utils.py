from passlib.context import CryptContext

# Create a CryptContext for password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    """
    Hashes a plain password using bcrypt.
    """
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str):
    """
    Verifies a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)