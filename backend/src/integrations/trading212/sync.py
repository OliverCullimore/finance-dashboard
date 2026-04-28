from src.accounts.schemas import AccountBase, AccountUpdate
from src.accounts.service import AccountService
from src.assets.schemas import AssetBase
from src.assets.service import AssetService
from src.connections.service import ConnectionService
from src.core.database import SessionLocal
from src.core.logging import logger
from src.core.utils import Source, decrypt
from src.integrations.trading212.client import Trading212Client, get_symbol_from_ticker
from src.integrations.trading212.mapper import map_account, map_dividend, map_order, map_position, map_transaction
from src.transactions.schemas import TransactionBase
from src.transactions.service import TransactionService


def sync():
    logger.info("Trading 212 sync started.")

    # Get DB connection
    db = SessionLocal()

    try:
        connection_service = ConnectionService(db, "sync")
        connections = connection_service.get_by_provider_for_sync(Source.TRADING212)
        for connection in connections:
            # Init Trading 212 client
            client = Trading212Client(decrypt(connection.api_key), decrypt(connection.api_secret))

            # Init services
            account_service = AccountService(db, connection.user_id)
            transaction_service = TransactionService(db, connection.user_id)
            asset_service = AssetService(db)

            # Get data
            account_data = client.get_account()
            position_data = client.get_positions()
            dividend_data = client.get_dividends()
            order_data = client.get_orders()
            transaction_data = client.get_transactions()

            # Debug
            # logger.info(json.dumps(account_data, indent=2))
            # logger.info(json.dumps(position_data, indent=2))
            # logger.info(json.dumps(dividend_data, indent=2))
            # logger.info(json.dumps(order_data, indent=2))
            # logger.info(json.dumps(transaction_data, indent=2))

            # Create/update account
            mapped = map_account(account_data)
            existing = account_service.get_by_external_id(Source.TRADING212, mapped["external_id"])
            if not existing:
                new_account = AccountBase(
                    connection_id=connection.id,
                    source=mapped["source"],
                    external_id=mapped["external_id"],
                    name=mapped["name"],
                    description=mapped["description"],
                    balance=mapped["balance"],
                    currency=mapped["currency"]
                )
                account = account_service.create(new_account)
            else:
                update_account = AccountUpdate(
                    balance=mapped["balance"],
                    currency=mapped["currency"]
                )
                account = account_service.update(existing.id, update_account)

            # Check account exists
            if account is not None:
                # Create/update assets from positions
                for position in position_data:
                    mapped = map_position(position)
                    new_asset = AssetBase(
                        symbol=get_symbol_from_ticker(mapped["symbol"]),
                        trading212_symbol=mapped["symbol"],
                        isin=mapped["isin"],
                        name=mapped["name"],
                        type=mapped["type"],
                        current_price=mapped["current_price"],
                        currency=mapped["currency"]
                    )
                    asset_service.upsert(new_asset)

                # Create/update transactions from dividends
                for dividend in dividend_data:
                    mapped = map_dividend(dividend)
                    asset = asset_service.get_by_isin(mapped["isin"])
                    new_transaction = TransactionBase(
                        external_id=mapped["external_id"],
                        type=mapped["type"],
                        amount=mapped["amount"],
                        currency=mapped["currency"],
                        description=mapped["description"],
                        asset_id=asset.id,
                        quantity=mapped["quantity"],
                        created_at=mapped["created_at"]
                    )
                    transaction_service.upsert(account.id, new_transaction)

                # Create/update transactions from orders
                for order in order_data:
                    if "fill" in order.keys():
                        mapped = map_order(order)
                        asset = asset_service.get_by_isin(mapped["isin"])
                        new_transaction = TransactionBase(
                            external_id=mapped["external_id"],
                            type=mapped["type"],
                            amount=mapped["amount"],
                            currency=mapped["currency"],
                            description=mapped["description"],
                            asset_id=asset.id,
                            quantity=mapped["quantity"],
                            price=mapped["price"],
                            created_at=mapped["created_at"]
                        )
                        transaction_service.upsert(account.id, new_transaction)

                # Create/update transactions from transactions
                for transaction in transaction_data:
                    mapped = map_transaction(transaction)
                    new_transaction = TransactionBase(
                        external_id=mapped["external_id"],
                        type=mapped["type"],
                        amount=mapped["amount"],
                        currency=mapped["currency"],
                        created_at=mapped["created_at"]
                    )
                    transaction_service.upsert(account.id, new_transaction)

    finally:
        db.close()
