from typing import List

from fastapi import APIRouter, HTTPException, Request

from src.accounts.schemas import (AccountBase, AccountResponse, AccountUpdate)
from src.accounts.service import AccountService
from src.core.database import db_dependency
from src.core.utils import authenticate_and_get_user_details

router = APIRouter()


@router.get("", response_model=List[AccountResponse])
def get_accounts(request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = AccountService(db, user_id)
    return service.get_all()


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = AccountService(db, user_id)
    account = service.get_by_id(account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account


@router.post("", response_model=AccountResponse)
def create_account(data: AccountBase, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = AccountService(db, user_id)
    return service.create(data)


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
        account_id: int,
        data: AccountUpdate,
        request: Request,
        db: db_dependency,
):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = AccountService(db, user_id)
    account = service.update(account_id, data)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account


@router.delete("/{account_id}")
def delete_account(account_id: int, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = AccountService(db, user_id)

    success = service.delete(account_id)

    if not success:
        raise HTTPException(status_code=404, detail="Account not found")

    return {"ok": True}
