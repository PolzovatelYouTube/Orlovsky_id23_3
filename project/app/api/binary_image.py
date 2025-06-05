from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.binary_image import BinaryImageRequest, BinaryImageTaskResponse
from app.core.celery_app import celery_app
from app.api.tasks import binarize_image_task

router = APIRouter()

@router.post("/binary_image", response_model=BinaryImageTaskResponse)
def binary_image(
    request: BinaryImageRequest,
    current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized user"
        )
    print(f"Current user: {current_user.email}")
    try:
        task = binarize_image_task.apply_async(args=[request.image, request.algorithm])
        return {
            "task_id": task.id,
            "status": "processing",
            "binarized_image": None,
            "error": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while starting the binarization task: {str(e)}"
        )

@router.get("/binary_image/status/{task_id}", response_model=BinaryImageTaskResponse)
def get_binary_image_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized user"
        )
    task_result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "status": task_result.state.lower(),
        "binarized_image": None,
        "error": None
    }
    if task_result.state == "FAILURE":
        response["status"] = "failed"
        response["error"] = str(task_result.result)
    elif task_result.state == "SUCCESS":
        result = task_result.result
        if isinstance(result, dict) and "binarized_image" in result:
            response["binarized_image"] = result["binarized_image"]
        response["status"] = "completed"
    return JSONResponse(content=response)
