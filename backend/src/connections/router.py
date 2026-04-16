from typing import List

from fastapi import APIRouter, HTTPException, Request

from src.connections.schemas import ConnectionResponse, ConnectionUpsert
from src.connections.service import ConnectionService
from src.core.database import db_dependency
from src.core.utils import authenticate_and_get_user_details

router = APIRouter()


@router.get("", response_model=List[ConnectionResponse])
def get_accounts(request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = ConnectionService(db, user_id)
    return service.get_all()


@router.post("", response_model=ConnectionUpsert)
def upsert_connection(data: ConnectionUpsert, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = ConnectionService(db, user_id)
    return service.upsert(data)


@router.delete("/{connection_id}")
def delete_connection(connection_id: int, request: Request, db: db_dependency):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    service = ConnectionService(db, user_id)

    success = service.delete(connection_id)

    if not success:
        raise HTTPException(status_code=404, detail="Connection not found")

    return {"ok": True}
