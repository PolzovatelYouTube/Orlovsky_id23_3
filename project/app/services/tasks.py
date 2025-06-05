from app.core.celery_app import celery_app
from app.services.binarization import binarize_image
import time

@celery_app.task(bind=True, name="app.services.tasks.binarize_image_task")
def binarize_image_task(self, image_data: str, algorithm: str) -> dict:
    # Имитация прогресса для демонстрации
    total_steps = 5
    for i in range(total_steps):
        time.sleep(0.5)  # имитация работы
        progress = int((i + 1) / total_steps * 100)
        self.update_state(state='PROGRESS', meta={'progress': progress})
    # Выполнение бинаризации
    binarized_image = binarize_image(image_data, algorithm)
    return {"status": "success", "binarized_image": binarized_image}

@celery_app.task(name="app.services.tasks.long_running_task")
def long_running_task(duration: int):
    import time
    time.sleep(duration)
    return {"status": "completed", "duration": duration}
