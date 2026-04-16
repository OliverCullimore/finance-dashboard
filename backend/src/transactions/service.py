from sqlalchemy.sql import func

from src.accounts.models import Account
from src.accounts.service import AccountService
from src.core.database import db_dependency
from src.core.logging import logger
from src.transactions.models import Transaction, TransactionType
from src.transactions.schemas import TransactionBase


class TransactionService:
    def __init__(self, db: db_dependency, user_id: str):
        self.db = db
        self.user_id = user_id

    def _base_query(self):
        return (
            self.db.query(Transaction)
            .join(Account, Transaction.account_id == Account.id)
            .filter(Account.user_id == self.user_id)
        )

    def get_all(self):
        return self._base_query().all()

    def get_all_by_account_id(self, account_id: int):
        return self._base_query().filter(Account.id == account_id).all()

    def get_by_id(self, account_id: int, transaction_id: int):
        return self._base_query().filter(
            Transaction.account_id == account_id,
            Transaction.id == transaction_id
        ).first()

    def get_positions_by_account_id(self, account_id: int):
        return (
            self._base_query()
            .with_entities(
                Transaction.asset_id,
                func.sum(Transaction.quantity).label("quantity"),
                (
                        func.sum(Transaction.quantity * Transaction.price)
                        / func.nullif(func.sum(Transaction.quantity), 0)
                ).label("avg_price"),
            )
            .filter(Transaction.account_id == account_id)
            .filter(Transaction.type == TransactionType.TRADE)
            .group_by(Transaction.asset_id)
            .all()
        )

    def upsert(self, account_id: int, data: TransactionBase):
        account_service = AccountService(self.db, self.user_id)
        account = account_service.get_by_id(account_id)
        if not account:
            logger.debug("Upsert failed. Account not found or not owned by user")
            return False

        transaction = self._base_query().filter(
            Transaction.account_id == account_id,
            Transaction.external_id == data.external_id
        ).first()

        if transaction:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(transaction, field, value)
        else:
            transaction = Transaction(**data.model_dump())
            transaction.account_id = account_id
            self.db.add(transaction)

        transaction.account_id = account_id
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, account_id: int, transaction_id: int):
        transaction = self.get_by_id(account_id, transaction_id)

        if not transaction:
            return False

        self.db.delete(transaction)
        self.db.commit()
        return True
