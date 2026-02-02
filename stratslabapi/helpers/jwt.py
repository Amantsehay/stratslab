from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt

from stratslabapi.core import settings


def _validate_secret_key(secret: str) -> str:
    """
    Validate the JWT secret key used for signing tokens.

    Enforces basic strength requirements to reduce the risk of using a
    weak or easily guessable key.
    """
    if not isinstance(secret, str):
        raise ValueError("JWT SECRET_KEY must be a string.")

    # Enforce a minimum length for the secret key.
    min_length = 32
    if len(secret) < min_length:
        raise ValueError(f"JWT SECRET_KEY must be at least {min_length} characters long.")

    # Require a minimum number of distinct characters to avoid trivial keys
    # such as repeating the same character.
    if len(set(secret)) < 8:
        raise ValueError("JWT SECRET_KEY must contain a diverse set of characters.")

    return secret


SECRET_KEY = _validate_secret_key(settings.secret_key.get_secret_value())
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, "access_token_expire_minutes", 30)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Invalid token")
