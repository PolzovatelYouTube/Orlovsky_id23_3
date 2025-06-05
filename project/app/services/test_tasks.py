from time import sleep
from app.core.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def test_task(self, duration):
    """
    Простая тестовая задача, которая "спит" указанное количество секунд.
    """
    logger.info(f"Task {self.request.id} started with duration {duration}")
    try:
        sleep(duration)
        logger.info(f"Task {self.request.id} completed")
        return f"Task completed after {duration} seconds"
    except Exception as e:
        logger.error(f"Task {self.request.id} failed: {e}")
        raise
