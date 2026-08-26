from datetime import datetime
from typing import Generic,List,Optional,TypeVar
from pydantic import BaseModel,ConfigDict,Field

T = TypeVar("T")

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True,populate_by_name=True)

class TimestampSchema(BaseModel):
    created_at:Optional[datetime]
    updated_at:Optional[datetime]


class MessageResponce(BaseModel):
    Message:str
    success:bool=True


class DataResponse(BaseModel,Generic[T]):
    success:bool=True
    message:str = "success"
    data:T


class PaginatedResponse(BaseModel,Generic[T]):
    items:List[T]
    total:int=Field(...,ge=0,description="Total no of records")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Items per page")
    total_pages: int = Field(..., ge=0, description="Total pages")
    has_next: bool = False
    has_prev: bool = False




