import enum

from clerk_backend_api import AuthenticateRequestOptions, Clerk
from cryptography.fernet import Fernet
from fastapi import HTTPException, Request
from sqlalchemy import Enum

from src.core.config import settings

clerk_sdk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)


def authenticate_and_get_user_details(request: Request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[settings.FRONTEND_HOST],
                jwt_key=settings.CLERK_JWT_KEY,
            )
        )
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_id = request_state.payload.get("sub")

        return {"user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class Source(enum.Enum):
    GOCARDLESS = "GoCardless"
    TRADING212 = "Trading 212"
    MANUAL = "Manual"


# Source enum
SourceEnum = Enum(Source, name="source")


class Currency(enum.Enum):
    GBP = "GBP"
    GBX = "GBX"
    EUR = "EUR"
    EUX = "EUX"
    USD = "USD"
    USX = "USX"


# Currency enum
CurrencyEnum = Enum(Currency, name="currency")

# Fernet
fernet = Fernet(settings.ENCRYPTION_KEY)


def encrypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()
