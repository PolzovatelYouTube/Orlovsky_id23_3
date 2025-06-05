from redislite import Redis
import os

# Определяем путь к базе данных Redis
redis_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "redis.db")
os.makedirs(os.path.dirname(redis_db_path), exist_ok=True)

# Инициализируем Redis с указанием пути к файлу базы данных
redis_server = Redis(redis_db_path)

# Формируем URL для доступа к Redis
if hasattr(redis_server, 'socket_file'):
    redis_url = f"redis+socket://{redis_server.socket_file}"
else:
    redis_url = "redis://localhost:6379"

# Путь к базе данных SQLite для Celery
celery_db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "results.sqlite")
celery_results_db_url = f"db+sqlite:///{celery_db_path}"