from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./brs_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)



def get_db_session():
    
    sess = Session(engine)
    return sess


def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

        
Base.metadata.create_all(bind=engine)