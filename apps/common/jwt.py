import time

import jwt

from apps.common.constants import JWT_ALGORITHM, JWT_EXPIRES_AT


class JWT:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        pass

    def encode(self, payload, token_type="access", algorithm=None):
        iat = int(time.time())
        id = getattr(payload, "id", None)
        if id is None:
            raise ValueError("Payload must have an id attribute")

        if algorithm is None:
            algorithm = JWT_ALGORITHM
        elif algorithm not in ("HS256", "HS512"):
            raise ValueError("Algorithm must be from the supported list")

        # Added logic for expiration
        expires_at = getattr(payload, "expires_at", None)
        expires_at_int = 0
        if expires_at is None:
            expires_at_int = (
                int(time.time()) + JWT_EXPIRES_AT
            )  # default expiration time: 1 day
        else:
            expires_at_int = int(expires_at)

        return jwt.encode(
            {
                "token_type": token_type,
                "user_id": str(id),
                "exp": expires_at_int,
                "iat": iat,
            },
            self.secret_key,
            algorithm=JWT_ALGORITHM,
        )

    def decode(self, token, algorithm=None):
        if token is None or token == "":
            raise ValueError("Token must be present and non-empty")

        if algorithm is None:
            algorithm = JWT_ALGORITHM
        elif algorithm not in ("HS256", "HS512"):
            raise ValueError("Algorithm must be from the supported list")

        # Added logic for decoding with expiration
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[algorithm], verify=True
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token is expired. Please generate a new one.")
