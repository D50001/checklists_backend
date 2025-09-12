import logging
from .celery import app as celery_app

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

__all__ = ("celery_app",)