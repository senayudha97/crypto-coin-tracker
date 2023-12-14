from typing import Optional
from fastapi import APIRouter, Depends
from dto.dto_coin import Coin


from dto.dto_common import TokenData
from services.service_coin import ServiceCoin
from services.service_common import get_current_user


router_coin = APIRouter(prefix="/api", tags=["Coin"])

@router_coin.get("/coin")
def get_coin(coin_id: Optional[str] = None, 
            current_user: TokenData = Depends(get_current_user), 
             service_coin: ServiceCoin = Depends()):
    return service_coin.get_coin(coin_id)

@router_coin.post("/coin")
def add_coin(input_coin: Coin,
            current_user: TokenData = Depends(get_current_user), 
            service_coin: ServiceCoin = Depends()):
    return service_coin.add_coin(input_coin, current_user)

@router_coin.get("/coin/tracked_coin")
def tracked_coin(coin_id: Optional[str] = None, 
            current_user: TokenData = Depends(get_current_user), 
             service_coin: ServiceCoin = Depends()):
    return service_coin.tracked_coin(coin_id, current_user)

# make feature for delete tracked coin 
@router_coin.delete("/coin/tracked_coin")
def delete_tracked_coin(id: str, 
            current_user: TokenData = Depends(get_current_user), 
             service_coin: ServiceCoin = Depends()):
    return service_coin.delete_tracked_coin(id, current_user)
