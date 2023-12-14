from typing import Optional
from fastapi import Depends, HTTPException
import requests
from dto.dto_coin import Coin

from dto.dto_common import TokenData
from repository.repository_coin import RepositoryCoin
from services.service_common import get_current_user



class ServiceCoin:
    def __init__(self, repository_coin : RepositoryCoin = Depends()) -> None:
        self.repository_coin = repository_coin
        self.exchange_api_url = "https://open.er-api.com/v6/latest/USD"
        
    def get_exchange_rate(self):
        response = requests.get(self.exchange_api_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch exchange rates")
        return response.json()['rates']['IDR']
        
    def get_coin(self, coin_id: Optional[str] = None):
        url = "https://api.coincap.io/v2/assets/"
    
        if coin_id is not None:
            url = url + coin_id

        headers = {
            'Authorization': 'Bearer 5d1b3255-6b10-4f4d-838f-95ec93830a49'
        }

        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Coin not found")
        
        coin_data = response.json()
        if coin_id is not None:
            usd_price = float(coin_data["data"]["priceUsd"])
            exchange_rate = self.get_exchange_rate()
            coin_data["data"]["priceIdr"] = usd_price * exchange_rate
        else:
            usd_price = float(coin_data["data"][0]["priceUsd"])
            exchange_rate = self.get_exchange_rate()
            index = 0
            for coin in coin_data["data"]:
                coin_data["data"][index]["priceIdr"] = float(coin["priceUsd"]) * exchange_rate
                index = index + 1

        return coin_data
    
    def validate_coin_id(self, coin_id: str):
        if coin_id is not None:
            coin = self.get_coin(coin_id)
            if coin is None:
                raise HTTPException(status_code=404, detail="Coin not found")
            return coin
        
    def add_coin(self, input_coin: Coin, current_user: TokenData = Depends(get_current_user)):
        coin = self.validate_coin_id(input_coin.coin_id)
        
        return self.repository_coin.add_coin(coin["data"], current_user)
    
    def tracked_coin(self, coin_id: Optional[str] = None, current_user: TokenData = Depends(get_current_user)):
        self.validate_coin_id(coin_id)
        
        return self.repository_coin.tracked_coin(coin_id, current_user)
    
    def delete_tracked_coin(self, id: str, current_user: TokenData = Depends(get_current_user)):
        
        return self.repository_coin.delete_tracked_coin(id, current_user)