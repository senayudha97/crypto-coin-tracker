from fastapi import Depends
from sqlalchemy.orm import Session


from dto.dto_user import InputLogin, InputUser
from models.model_users import DATABASE_URL, SessionLocal, engine, Base, Users
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RepositoryUser:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = db
    
    def insert_new_user(self, new_user: InputUser):
        new_user = new_user.model_dump()
        del new_user["confirm_password"]
        
        db_item = Users(**new_user)
        self.repository.add(db_item)
        self.repository.commit()
        self.repository.refresh(db_item)
        return db_item
    
    def find_user_by_username_password(self, input_login: InputLogin):
        result = self.repository.query(Users).filter(Users.username == input_login.username, Users.password == input_login.password).first()
        if result is not None:
            return result
        return None 

    def find_user_by_username(self, username:str):
        result = self.repository.query(Users).filter(Users.username == username).first()
        if result is not None: 
            return result
        return None
        
    
    
    