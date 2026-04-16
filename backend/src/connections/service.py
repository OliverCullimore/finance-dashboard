from src.connections.models import Connection
from src.connections.schemas import ConnectionUpsert
from src.core.database import db_dependency
from src.core.utils import Source, encrypt


class ConnectionService:
    def __init__(self, db: db_dependency, user_id: str):
        self.db = db
        self.user_id = user_id

    def _base_query(self):
        return (
            self.db.query(Connection)
            .filter(Connection.user_id == self.user_id)
        )

    def get_all(self):
        return self._base_query().all()

    def get_by_id(self, connection_id: int):
        return self._base_query().filter(Connection.id == connection_id).first()

    def get_by_provider(self, provider: Source):
        return self._base_query().filter(Connection.provider == provider).first()

    def get_by_provider_for_sync(self, provider: Source):
        if self.user_id != "sync":
            return False
        return self.db.query(Connection).filter(Connection.provider == provider).all()

    def upsert(self, data: ConnectionUpsert):
        connection = self.get_by_provider(Source[data.provider])

        if connection:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(connection, field, value)
        else:
            connection = Connection(**data.model_dump())
            connection.user_id = self.user_id
            self.db.add(connection)

        connection.user_id = self.user_id
        # Encrypt data
        if connection.api_key is not None:
            connection.api_key = encrypt(connection.api_key)
        if connection.api_secret is not None:
            connection.api_secret = encrypt(connection.api_secret)
        if connection.access_token is not None:
            connection.access_token = encrypt(connection.access_token)
        if connection.refresh_token is not None:
            connection.refresh_token = encrypt(connection.refresh_token)
        self.db.commit()
        self.db.refresh(connection)
        return connection

    def delete(self, connection_id: int):
        connection = self.get_by_id(connection_id)

        if not connection:
            return False

        self.db.delete(connection)
        self.db.commit()
        return True
