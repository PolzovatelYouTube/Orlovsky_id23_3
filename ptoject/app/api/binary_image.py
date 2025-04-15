from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.binary_image import BinaryImageRequest, BinaryImageResponse
from app.services.binarization import binarize_image

router = APIRouter()

@router.post("/binary_image", response_model=BinaryImageResponse)
def binary_image(
    request: BinaryImageRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        binarized_image = binarize_image(request.image, request.algorithm)
        return {"binarized_image": binarized_image}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during image binarization: {str(e)}"
        )