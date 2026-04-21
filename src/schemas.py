from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Optional
from enum import Enum

class PriorityEnum(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class SeverityEnum(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class BugReportCreate(BaseModel):
    email: EmailStr
    author: str
    release_build_no: str
    fixed_by: Optional[str] = None
    open_date: date
    close_date: Optional[date] = None
    description: str
    priority: PriorityEnum
    severity: SeverityEnum
    # Список выбранных типов дефектов (чекбоксы на макете)
    defect_types: List[str] 

class BugReportResponse(BugReportCreate):
    id: int

    class Config:
        from_attributes = True