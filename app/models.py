from pydantic import BaseModel
from typing import Optional
from typing import List
from datetime import date
from enum import Enum

# Enum pour forcer des choix dans certain champ
class Priority(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

class Status(str, Enum):
    Open = "Open"
    InProgress = "In progress"
    Closed = "Done"



# Pydantic sert a protege mes inputs avec la creation de Modeles
class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Priority
    status: Status
    tags: List[str]
    createdAt: date

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    tags: Optional[list[str]] = None

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    tags: list[str]
    createdAt: str