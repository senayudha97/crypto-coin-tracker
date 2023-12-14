from sqlalchemy import Column, Integer, String, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./verihubs-coding-test.db"

Base = declarative_base()

class Coins(Base):
    __tablename__ = "tracked_coins"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    coin_id = Column(String, nullable=False)
    coin_symbol = Column(String, nullable=False)
    coin_name = Column(String, nullable=False)
    coin_price_idr = Column(Float, nullable=False)
    created_at = Column(String, nullable=False)
    

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
