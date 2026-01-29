from fastapi import FastAPI
from routes import routes
from config.mongo_manager import mongo_manager

app = FastAPI()

@app.on_event("startup")
async def startup():
    mongo_manager.connect()

@app.on_event("shutdown")
async def shutdown():
    mongo_manager.close()

app.include_router(routes.url_shortener_routes)