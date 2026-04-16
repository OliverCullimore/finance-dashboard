import logging

from src.core.config import settings

logging.basicConfig(
    level=logging.getLevelName(settings.LOG_LEVEL)
)

logger = logging.getLogger(__name__)
