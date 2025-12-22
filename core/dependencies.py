from functools import lru_cache
from typing import Generator

from core.database import SessionLocal

from core.bio_service import BioService
from config import settings

def get_db() -> Generator:
    """
    Creates a new database session for a request, yields it to the route,
    and guarantees it is closed after the request finishes.
    """
    db = SessionLocal()
    try:
        # 'yield' acts like a pause button. It gives the db to the route.
        # The code stops here until the route is finished.
        yield db
    finally:
        # This block runs after the request is done, no matter what.
        db.close()

@lru_cache()
def get_bio_service() -> BioService:
    """
    Creates a SINGLE instance of BioService.
    Because of @lru_cache, this function executes only once.
    Every subsequent call returns the specific instance created the first time.
    """
    # You might want to pass config settings here if your service needs them
    return BioService(model_path=settings.MODEL_CACHE_DIR)