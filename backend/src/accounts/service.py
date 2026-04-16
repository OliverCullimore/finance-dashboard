from src.accounts.models import Account
from src.accounts.schemas import AccountBase, AccountUpdate
from src.core.database import db_dependency
from src.core.utils import Source


class AccountService:
    def __init__(self, db: db_dependency, user_id: str):
        self.db = db
        self.user_id = user_id

    def get_all(self):
        return self.db.query(Account).filter(Account.user_id == self.user_id).all()

    def get_by_id(self, account_id: int):
        return self.db.query(Account).filter(
            Account.user_id == self.user_id,
            Account.id == account_id
        ).first()

    def get_by_external_id(self, source: Source, external_id: str):
        return self.db.query(Account).filter(
            Account.user_id == self.user_id,
            Account.source == source,
            Account.external_id == external_id
        ).first()

    def create(self, data: AccountBase):
        account = Account(**data.model_dump())
        account.user_id = self.user_id
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, account_id: int, data: AccountUpdate):
        account = self.get_by_id(account_id)

        if not account:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(account, field, value)

        account.user_id = self.user_id
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete(self, account_id: int):
        account = self.get_by_id(account_id)

        if not account or not account.user_id == self.user_id:
            return False

        self.db.delete(account)
        self.db.commit()
        return True
