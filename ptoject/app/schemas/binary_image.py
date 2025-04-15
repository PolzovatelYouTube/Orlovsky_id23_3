from pydantic import BaseModel
from typing import Optional

class BinaryImageRequest(BaseModel):
    image: str  # base64 encoded image
    algorithm: str = "otsu"  # default algorithm

class BinaryImageResponse(BaseModel):
    binarized_image: str  # base64 encoded binarized image