from datetime import datetime
from typing import Optional, List, Dict, Any

from models import TodoTask
from pydantic import BaseModel

class TodoTaskCreate(BaseModel):
    id : Optional[int]= None
    task_name: str
    status: str
    user_id: Optional[int] =None
    created_at: datetime

    class Config:
        orm_mode = True

class TodoTaskBase(TodoTaskCreate):
    class Config:
        orm_mode = True

class FieldModelCreate(BaseModel):
    field_name: str
    field_rename: str
    field_type: str
    field_is_active: bool

    class Config:
        orm_mode = True

class SectionModelCreate(BaseModel):
    section_name: str
    section_rename: str
    section_is_active: bool
    section_fields: List[FieldModelCreate]

    class Config:
        orm_mode = True

class TabModelCreate(BaseModel):
    tab_name: str
    tab_rename: str
    tab_is_active: bool
    tab_sections: Optional[List[SectionModelCreate]] = None

    class Config:
        orm_mode = True

class TemplateModelCreate(BaseModel):
    name: str
    rename: str
    tabs: List[TabModelCreate]

    class Config:
        orm_mode = True

class FormDataCreate(BaseModel):
    template_name: str
    data: Dict[str, Any]

    class Config:
        orm_mode = True