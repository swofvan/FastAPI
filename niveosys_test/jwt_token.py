from jose import jwt

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"


def create_access_token(data):

    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token