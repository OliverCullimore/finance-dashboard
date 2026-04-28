import json

import yfinance as yf_client

from src.assets.models import Asset, AssetType
from src.assets.schemas import AssetBase
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

    # Init services
    asset_service = AssetService(db)
    sector_service = SectorService(db)
    industry_service = IndustryService(db)

    # Get assets
    assets = asset_service.get_all_for_yahoo_finance_sync()
    for asset in assets:
        logger.info(f"Looking up asset {asset.symbol} {asset.isin}")

        yf_sector_industry = get_yf_sector_industry(asset)
        sector = yf_sector_industry.get("sector")
        industry = yf_sector_industry.get("industry")
        if sector and industry:
            # Ensure sector exists
            new_sector = SectorBase(name=sector)
            sector = sector_service.upsert(new_sector)

            # Ensure industry exists (normalize first)
            industry = industry.replace("—", "-")
            new_industry = IndustryBase(name=industry)
            industry = industry_service.upsert(new_industry)

            # Update asset
            upsert_asset = AssetBase(
                sector_id=sector.id,
                industry_id=industry.id,
                isin=asset.isin,
                type=AssetType(asset.type).name
            )
            asset_service.upsert(upsert_asset)
        else:
            logger.info(f"Yahoo missing sector/industry for {asset.symbol}")


def get_yf_sector_industry(asset: Asset) -> dict:
    try:
        yh_ticker = yf_client.Ticker(asset.symbol)
        yh_ticker_info = yh_ticker.get_info()
        sector = yh_ticker_info.get("sector")
        industry = yh_ticker_info.get("industry")
        if sector and industry:
            return {"sector": sector, "industry": industry}
        else:
            yh_search = yf_client.Search(
                asset.isin,
                news_count=0,
                lists_count=0,
                include_cb=False,
                recommended=0
            ).quotes
            logger.debug(json.dumps(yh_search, indent=2))
            if yh_search[0]:
                sector = yh_search[0].get("sector")
                industry = yh_search[0].get("industry")
                if sector and industry:
                    return {"sector": sector, "industry": industry}

        return {}

    except Exception as e:
        logger.warning(
            f"Yahoo lookup failed for {asset.symbol} {asset.isin} {asset.currency.value} {asset.name} {asset.trading212_symbol}: {e}")
