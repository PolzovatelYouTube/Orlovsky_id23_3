from celery import Celery
from app.core.redis_server import redis_url, celery_results_db_url

celery_app = Celery(
    "binarization_api",
    broker=redis_url,
    backend=celery_results_db_url,  # Используем переменную с путем к базе данных
    include=["app.services.tasks", "app.services.test_tasks"]
)

# Ограничение количества одновременно работающих процессов воркера Celery до 2
celery_app.conf.update(
    worker_concurrency=2,
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_default_queue='celery',
    task_routes={
        'app.services.tasks.long_running_task': {'queue': 'celery'},
        'app.services.test_tasks.test_task': {'queue': 'celery'},
    }
)