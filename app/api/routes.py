from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.engine import get_db
from app.db.models import Client, create_table, Case, Hearing, Note
from app.schema.schema import ClientDet,CaseDet,ClientRes,HearingDet,CaseRes,NoteDet,HearingRes,NoteRes
from sqlalchemy import select,asc,delete
from typing import List
from datetime import date


router = APIRouter()

@router.get('/')
def home():
    return {'message':'Hello From Server'}

@router.get('/create-table')
def start():
    create_table()
    return {"message":"Tables created"}

# New Client addition
@router.post('/add-client')
def add_client(info:ClientDet,db:Session=Depends(get_db)):
    try:
        new=Client(name=info.name,contact=info.contact)
        db.add(new)
        db.commit()
        db.refresh(new)
        return {"message":True}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="could not add client"
        )
    
# endpoint for every client in database
@router.get('/get-clients',response_model=List[ClientRes])
def get_clients(db:Session=Depends(get_db)):
    try:
        data=select(Client)
        clients=db.scalars(data).all()

        return clients
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="couldn't fetch client details"
        )

# getting Client details by searching
@router.get('/client-details',response_model=List[ClientRes])
def client_details(name:str,db:Session=Depends(get_db)):
    data=select(Client).where(Client.name==name)
    clients=db.scalars(data).all()

    return clients

# Adding Cases to Clients
@router.post('/add-case')
def add_case(info:CaseDet,db:Session=Depends(get_db)):
    try:
        data=Case(**info.model_dump())
        db.add(data)
        db.commit()
        # db.refresh(data)

        return {"message":True}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="details could not be added"
        )
    
# endpoint to get case details filtered by client
@router.get('/get-cases-client',response_model=List[CaseRes])
def get_cases_client(id:int,db:Session=Depends(get_db)):
    data=select(Case).where(Case.client_id==id)
    cases=db.scalars(data).all()
    return cases
    
# *********************************************************************************
# Hearing routes only
# *********************************************************************************

# getting caseid for hearing and notes attaching purposed
@router.get('/case-details',response_model=CaseRes)
def case_details(casenumber:str,db:Session=Depends(get_db)):
    data=select(Case).where(Case.case_number==casenumber)
    case=db.scalars(data).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    return case
    
# Adding hearing details and modifying on Case Table
@router.post('/add-hearing')
def add_hearing(info:HearingDet,db:Session=Depends(get_db)):
    data=Hearing(**info.model_dump())
    db.add(data)
    case_id=info.case_id
    case_data=db.get(Case,case_id)

    if not case_data:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if case_data.next_hearing_date is None or info.hearing_date > date.today():
        case_data.next_hearing_date=info.hearing_date
    
    if case_data.status != info.status:
        case_data.status= info.status

    db.commit()
    return {'message':"updated successfully"}

@router.get('/get-hearings',response_model=List[HearingRes])
def get_hearings(db:Session=Depends(get_db)):
    data = select(Hearing).order_by(asc(Hearing.hearing_date))
    datas = db.scalars(data).all()
    return datas

# exposing hearing details sorted by asc filter by client
@router.get('/get-hearing-case',response_model=List[HearingRes])
def get_hearing_case(id:int,db:Session=Depends(get_db)):
    data=select(Hearing).where(Hearing.case_id==id).order_by(asc(Hearing.hearing_date))
    details=db.scalars(data).all()

    return details



# Adding notes to cases 
@router.post('/add-notes')
def add_notes(info:NoteDet,db:Session=Depends(get_db)):
    try:
        data=Note(**info.model_dump())
        db.add(data)
        db.commit()
        return {"message":True}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="notes could not be added"
        )

# get notes per case
@router.get('/get-notes',response_model=List[NoteRes])
def get_notes(id:int,db:Session=Depends(get_db)):
    data=select(Note).where(Note.case_id==id)
    notes=db.scalars(data).all()

    return notes

# ******************************************************************
# Delete Routes
# ******************************************************************

# delete notes
@router.delete('/delete-notes')
def delete_notes(id:int,db:Session=(Depends(get_db))):
    note=db.get(Note,id)
    if note:
        db.delete(note)
        db.commit()
    return {"message":True}

# delete cases
@router.delete('/delete-cases')
def delete_case(id: int, db: Session = Depends(get_db)):
    case = db.get(Case, id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    db.execute(delete(Note).where(Note.case_id == id))
    db.execute(delete(Hearing).where(Hearing.case_id == id))
    db.delete(case)
    db.commit()
    return {"message": True}

# delete clients
@router.delete('/delete-client')
def delete_client(id:int,db:Session=Depends(get_db)):
    client=db.get(Client,id)
    if not client:
        raise HTTPException(status_code=404, detail="Case not found")
    cases=delete(Case).where(Case.client_id==id)
    notes=delete(Note).where(Note.case_id.in_(
        select(Case.id).where(Case.client_id==id)
    ))
    db.execute(notes)
    
    db.execute(cases)

    db.delete(client)
    db.commit()
    return {"message":True} 


# *******************************************************
# MODIFY DATA
# *******************************************************

# Only client contact can be modified
@router.put('/update_client_det')
def update_client_det(id:int,contact:str,db:Session=Depends(get_db)):
    user=db.get(Client,id)
    if user:
        user.contact=contact
        db.commit()
        return {'message':True}
    else:
        return {'message':False}
    
# Note content is modifiable
@router.put('/update_note_content')
def update_note_content(id:int,content:str,db:Session=Depends(get_db)):
    data=db.get(Note,id)
    if data:
        data.content=content
        db.commit()
        return {'message':True}
    else:
        return {'message':False}
    
# Only title and court namee is editable in case details
@router.put('/update_case_details')
def update_case_details(id:int,new_title:str,new_court:str,db:Session=Depends(get_db)):
    data=db.get(Case,id)
    if data:
        data.title=new_title
        data.court_name=new_court
        db.commit()
        return {'message':True}
    else:
        return {'message':False}
    
# Only description editable in Hearings table
@router.put('/update_hearings_desc')
def update_hearings_desc(id:int,content:str,db:Session=Depends(get_db)):
    data=db.get(Hearing,id)
    if data:
        data.description=content
        db.commit()
        return {'message':True}
    else:
        return {'message':False}