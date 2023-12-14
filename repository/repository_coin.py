from typing import Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from dto.dto_common import TokenData            
from datetime import datetime

from models.model_coins import DATABASE_URL, SessionLocal, engine, Base, Coins
from services.service_common import get_current_user
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RepositoryCoin:
    def __init__(self, db: Session = Depends(get_db)):
        self.repository = db
    
    def add_coin(self, coin, current_user: TokenData = Depends(get_current_user)):   
        new_tracked_coin = {
            "user_id": current_user.userId,
            "coin_id": coin["id"],
            "coin_symbol": coin["symbol"],
            "coin_name": coin["name"],
            "coin_price_idr": coin["priceIdr"],
            "created_at": datetime.utcnow(),
        }
        
        db_item = Coins(**new_tracked_coin)
        self.repository.add(db_item)
        self.repository.commit()
        self.repository.refresh(db_item)
        
        return db_item
    
    def tracked_coin(self, coin_id: Optional[str] = None, current_user: TokenData = Depends(get_current_user)):
        if coin_id is None:
            return self.repository.query(Coins).filter(Coins.user_id == current_user.userId).all()
        
        return self.repository.query(Coins).filter(Coins.user_id == current_user.userId, Coins.coin_id == coin_id).all()
    
    def delete_tracked_coin(self, id: str, current_user: TokenData = Depends(get_current_user)):
        deleted_rows = self.repository.query(Coins).filter(Coins.user_id == current_user.userId, Coins.id == id).delete()
        self.repository.commit()
        if deleted_rows == 0:
            return {"message": "No data deleted"}
        
        return {"message": "Data deleted successfully"}
            
    