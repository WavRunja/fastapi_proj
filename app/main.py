# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users

# Создаем таблицы (пока синхронно)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Mini App")

# Подключаем роутеры
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в FastAPI mini app!"}
