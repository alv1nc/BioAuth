from functools import lru_cache
from typing import Generator

from core.bio_service import BioAuthService
from core.config import settings

@lru_cache()
def get_service() -> BioAuthService:
    """
    Creates a SINGLE instance of BioService.
    Because of @lru_cache, this function executes only once.
    Every subsequent call returns the specific instance created the first time.
    """
    # You might want to pass config settings here if your service needs them
    return BioAuthService(settings.SPEECHBRAIN_DIR)