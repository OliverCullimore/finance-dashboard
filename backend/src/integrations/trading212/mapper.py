from src.assets.models import AssetType
from src.core.utils import Source
from src.transactions.models import TransactionType


def map_account(api_data) -> dict:
    return {
        "source": Source.TRADING212.name,
        "external_id": str(api_data["id"]),
        "name": "Trading 212",
        "description": "Invest and Stocks ISA",
        "balance": api_data["cash"]["availableToTrade"],
        "currency": api_data["currency"],
    }


def map_position(api_data) -> dict:
    return {
        "symbol": api_data["instrument"]["ticker"],
        "isin": api_data["instrument"]["isin"],
        "name": api_data["instrument"]["name"],
        "type": AssetType.STOCK.name,
        "current_price": api_data["currentPrice"],
        "currency": api_data["instrument"]["currency"],
    }


def map_dividend(api_data) -> dict:
    return {
        "external_id": api_data["reference"],
        "type": TransactionType.DIVIDEND.name,
        "amount": api_data["amount"],
        "currency": api_data["currency"],
        "description": api_data["type"],
        "isin": api_data["instrument"]["isin"],
        "quantity": api_data["quantity"],
        "created_at": api_data["paidOn"]
    }


def map_order(api_data) -> dict:
    return {
        "external_id": str(api_data["fill"]["id"]),
        "type": TransactionType.TRADE.name,
        "amount": api_data["fill"]["walletImpact"]["netValue"],
        "currency": api_data["fill"]["walletImpact"]["currency"],
        "description": api_data["fill"]["type"],
        "isin": api_data["order"]["instrument"]["isin"],
        "quantity": api_data["fill"]["quantity"],
        "price": api_data["fill"]["price"],
        "created_at": api_data["fill"]["filledAt"]
    }


def map_transaction(api_data) -> dict:
    return {
        "external_id": api_data["reference"],
        "type": api_data["type"],
        "amount": api_data["amount"],
        "currency": api_data["currency"],
        "created_at": api_data["dateTime"]
    }
