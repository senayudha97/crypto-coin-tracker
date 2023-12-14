from fastapi import FastAPI
from routes.router_coin import router_coin
from routes.router_user import router_user


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Coin Tracking API!", "author": "Sena Yudha", "about": "Verihubs Coding Test"}
    

app.include_router(router_user)
app.include_router(router_coin)
