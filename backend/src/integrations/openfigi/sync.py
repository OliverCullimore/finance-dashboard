import json

from src.assets.schemas import AssetBase
from src.assets.service import AssetService
from src.core.config import settings
from src.core.database import SessionLocal
from src.core.logging import logger
from src.integrations.openfigi.client import OpenFIGIClient


def sync():
    logger.info("OpenFIGI sync started.")

    # Get DB connection
    db = SessionLocal()

    try:
        # Init OpenFIGI client
        client = OpenFIGIClient(settings.OPENFIGI_API_KEY)

        # Init services
        asset_service = AssetService(db)

        # Get assets
        assets = asset_service.get_all_for_openfigi_sync()
        for asset in assets:
            logger.info(f"Looking up asset {asset.trading212_symbol} {asset.isin}")
            try:
                symbol_results = client.get_isin_mapping(asset.isin)
                if symbol_results[0]["data"]:
                    symbol = client.pick_primary_isin_mapping(symbol_results[0]["data"])
                    symbol_ticker = symbol.get("ticker")
                    if symbol_ticker:
                        # Update asset
                        upsert_asset = AssetBase(
                            symbol=symbol_ticker,
                            isin=asset.isin,
                            type=asset.type
                        )
                        asset_service.upsert(upsert_asset)
                    else:
                        logger.info(f"OpenFIGI missing symbol for {asset.trading212_symbol} {asset.isin}")
                else:
                    logger.debug(json.dumps(symbol_results[0]["data"], indent=2))
            except Exception as e:
                logger.warning(f"OpenFIGI lookup failed for {asset.trading212_symbol} {asset.isin}: {e}")

    finally:
        db.close()
