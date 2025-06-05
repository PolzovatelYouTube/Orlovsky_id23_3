from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from app.services.tasks import long_running_task
from app.services.binarization import binarize_image
from app.core.celery_app import celery_app
from app.services.test_tasks import test_task

router = APIRouter()

@router.post("/start")
async def start_task(duration: int = 10):
    """
    Запускает длительную задачу с указанной длительностью (в секундах).
    Возвращает task_id для отслеживания статуса.
    """
    print(f"Sending long_running_task with duration {duration}")
    task = long_running_task.apply_async(args=[duration])
    print(f"Task sent with id {task.id}")
    return {"task_id": task.id}

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Возвращает статус и результат задачи по task_id.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "state": task_result.state,
        "progress": 0,
        "result": None,
        "error": None,
        "info": {}
    }
    if task_result.state == "PROGRESS":
        response["progress"] = task_result.info.get("progress", 0)
    elif task_result.state == "FAILURE":
        response["error"] = str(task_result.result)
    elif task_result.state == "SUCCESS":
        response["result"] = task_result.result
        response["progress"] = 100
    return response

@celery_app.task(name="app.services.tasks.binarize_image_task")
def binarize_image_task(image_data: str, algorithm: str) -> dict:
    # Здесь вызывается ваша функция бинаризации
    binarized_image = binarize_image(image_data, algorithm)
    return {"status": "success", "binarized_image": binarized_image}