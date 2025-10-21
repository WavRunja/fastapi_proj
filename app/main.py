from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Mini App")

# Подключаем роутеры
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Добро пожаловать в FastAPI mini app!"}
