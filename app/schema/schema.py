from pydantic import BaseModel,ConfigDict
from datetime import datetime,date
from typing import Optional

class Base(BaseModel):

    pass


class LawyerInp(Base):

    name:str
    email:str

class ClientDet(Base):

    name:str
    contact:str

class ClientRes(Base):

    id:int
    name:str
    contact:str

    model_config=ConfigDict(from_attributes=True)

class CaseDet(Base):

    title:str
    case_number:str
    client_id:int
    court_name:str
    status:str
    next_hearing_date:Optional[date] = None

class CaseRes(Base):
    id:int
    title:str
    case_number:str
    client_id:int
    court_name:str
    status:str
    next_hearing_date:Optional[date] = None

    model_config=ConfigDict(from_attributes=True)

class HearingDet(Base):

    case_id:int
    hearing_date:date
    description:str
    status:str
    result:str

class HearingRes(Base):

    id:int
    case_id:int
    hearing_date:date
    description:str
    status:str
    result:str

    model_config=ConfigDict(from_attributes=True)

# class TaskDet(Base):

#     id: int
#     title: str 
#     description:str
#     caseid:int
#     duedate:date
#     status:str
#     priority:str
#     createdat:datetime

class NoteDet(Base):
                      
    case_id:int
    content:str

class NoteRes(Base):
    id:int
    case_id:int
    content:str
    created_at:datetime