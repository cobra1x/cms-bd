from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url="sqlite:///sqlite.db"

engine=create_engine(db_url,echo=True)

SessionLocal=sessionmaker(bind=engine,expire_on_commit=True)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

