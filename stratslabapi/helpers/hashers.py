from passlib.context import CryptContext


class PasswordHasherBase:
    """Base class for password hashing"""

    def hash(self, password: str) -> str:
        """Hash a password"""
        raise NotImplementedError

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        raise NotImplementedError


class BcryptHasher(PasswordHasherBase):
    """Bcrypt password hasher"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a bcrypt hash"""
        return self.pwd_context.verify(plain_password, hashed_password)


# Global hasher instance
hasher = BcryptHasher()
