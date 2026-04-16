from typing import List

from fastapi import APIRouter, HTTPException, Request

from src.core.database import db_dependency
from src.core.utils import authenticate_and_get_user_details
from src.transactions.schemas import PositionBase, TransactionResponse
from src.transactions.service import TransactionService

router = APIRouter()


@router.get("", response_model=List[TransactionResponse])
def get_transactions(request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = TransactionService(db, user_id)
    transactions = service.get_all()

    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found")

    return transactions


@router.get("/{account_id}", response_model=List[TransactionResponse])
def get_transactions_by_account(account_id: int, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = TransactionService(db, user_id)
    transactions = service.get_all_by_account_id(account_id)

    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found")

    return transactions


@router.get("/{account_id}/positions", response_model=List[PositionBase])
def get_positions_by_account(account_id: int, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = TransactionService(db, user_id)
    positions = service.get_positions_by_account_id(account_id)

    if not positions:
        raise HTTPException(status_code=404, detail="Positions not found")

    return positions


@router.get("/{account_id}/{transaction_id}", response_model=TransactionResponse)
def get_account_transaction(account_id: int, transaction_id: int, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = TransactionService(db, user_id)
    transaction = service.get_by_id(account_id, transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction
