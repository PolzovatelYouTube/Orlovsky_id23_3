# app/schemas/binary_image.py
from pydantic import BaseModel
from typing import Optional

class BinaryImageRequest(BaseModel):
    image: str  # base64 encoded image
    algorithm: str = "otsu"  # default algorithm

class BinaryImageResponse(BaseModel):
    binarized_image: str  # base64 encoded binarized image
    
class BinaryImageTaskResponse(BaseModel):
    task_id: str
    status: str  # processing, completed, failed
    binarized_image: Optional[str] = None
    error: Optional[str] = None