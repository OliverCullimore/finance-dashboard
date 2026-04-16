from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.integrations.openfigi.sync import sync as sync_openfigi
from src.integrations.trading212.sync import sync as sync_trading212
from src.integrations.yahoofinance.sync import sync as sync_yahoofinance

scheduler = AsyncIOScheduler()


def start_scheduler():
    sync_openfigi()
    # sync_yahoofinance()
    scheduler.add_job(sync_trading212, "interval", minutes=15)
    scheduler.add_job(sync_openfigi, "interval", minutes=15)
    scheduler.add_job(sync_yahoofinance, "interval", minutes=15)

    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown()
