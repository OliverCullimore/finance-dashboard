import yfinance as yf_client

from src.assets.service import AssetService
from src.core.database import SessionLocal
from src.core.logging import logger
from src.industries.schemas import IndustryBase
from src.industries.service import IndustryService
from src.sectors.schemas import SectorBase
from src.sectors.service import SectorService


def sync():
    logger.info("Yahoo Finance sync started.")

    # Get DB connection
    db = SessionLocal()

    try:
        # Init services
        asset_service = AssetService(db)
        sector_service = SectorService(db)
        industry_service = IndustryService(db)

        # Get assets
        assets = asset_service.get_all_for_yahoo_finance_sync()
        for asset in assets:
            logger.info(f"Looking up asset {asset.symbol} {asset.isin}")
            try:
                normalized_symbol = asset.symbol.split("_")[0]
                yh_ticker = yf_client.Ticker(normalized_symbol)
                yh_ticker_info = yh_ticker.info or {}
                sector = yh_ticker_info.get("sector")
                industry = (
                    yh_ticker_info.get("industry")

                )
                if sector and industry:
                    # Ensure sector exists
                    new_sector = SectorBase(
                        name=sector
                    )
                    sector = sector_service.upsert(new_sector)

                    # Ensure industry exists (normalize first)
                    industry = industry.lower().replace("—", "-").replace(" ", "_").replace("-", "_")
                    new_industry = IndustryBase(
                        name=industry
                    )
                    industry = industry_service.upsert(new_industry)

                    # Update asset
                    asset.sector_id = sector.id
                    asset.industry_id = industry.id
                    asset_service.upsert(asset)
                else:
                    logger.info(f"Yahoo missing sector/industry for {asset.symbol}")
            except Exception as e:
                logger.warning(f"Yahoo lookup failed for {asset.symbol}: {e}")

    finally:
        db.close()
