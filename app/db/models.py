from app.db.engine import engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy.types import String,Date,DateTime,Text
from sqlalchemy import ForeignKey
import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class Lawyer(Base):
    __tablename__= "lawyers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False,default="admin")
    email: Mapped[str] = mapped_column(String,nullable=False,unique=True,default="admin@legalmate.ai")

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    contact: Mapped[str] = mapped_column(String(10),nullable=False)

class Case(Base):
    __tablename__="cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    case_number: Mapped[str] = mapped_column(String,nullable=False,unique=True)
    client_id:Mapped[int]=mapped_column(ForeignKey("clients.id"))
    court_name:Mapped[str]=mapped_column(String,nullable=False)
    status:Mapped[str]=mapped_column(String,nullable=False)
    next_hearing_date:Mapped[datetime.date]=mapped_column(Date,nullable=True)
    last_updated:Mapped[datetime.datetime]=mapped_column(DateTime,nullable=False,default=datetime.datetime.now,onupdate=datetime.datetime.now)

    # hearing:Mapped[List["Hearing"]]=relationship(back_populates="case")

class Hearing(Base):
    __tablename__= "hearings"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id:Mapped[int]=mapped_column(ForeignKey("cases.id"))
    hearing_date:Mapped[datetime.date]=mapped_column(Date,nullable=False)
    description:Mapped[str]=mapped_column(Text,nullable=False)
    result:Mapped[str]=mapped_column(String,nullable=False)
    status:Mapped[str]=mapped_column(String,nullable=False)
    # case:Mapped["Case"]= relationship(back_populates="hearing")

# class Task(Base):
#     __tablename__="tasks"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(30), nullable=False)
#     description:Mapped[str]=mapped_column(Text,nullable=False)
#     case_id:Mapped[int]=mapped_column(ForeignKey("cases.id"),nullable=True)
#     due_date:Mapped[datetime.date]=mapped_column(Date,nullable=False)
#     status:Mapped[str]=mapped_column(String,nullable=False)
#     priority:Mapped[str]=mapped_column(String,nullable=False)
#     created_at:Mapped[datetime.datetime]=mapped_column(DateTime,nullable=False,default=datetime.datetime.now)

class Note(Base):
    __tablename__="notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id:Mapped[int]=mapped_column(ForeignKey("cases.id"))
    content:Mapped[str]=mapped_column(Text,nullable=False)
    created_at:Mapped[datetime.datetime]=mapped_column(DateTime,nullable=False,default=datetime.datetime.now)

def create_table():
    Base.metadata.create_all(engine)