from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Watt Logic API")

# Для связи с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Добавим тестовые товары, если БД пуста
    from .database import SessionLocal
    from . import models
    db = SessionLocal()
    if not db.query(models.Product).first():
        test_products = [
            models.Product(name="MagSafe Charger", description="Беспроводная зарядка", price=39.99),
            models.Product(name="USB-C Hub", description="Хаб на 7 портов", price=79.99),
            models.Product(name="LED Desk Lamp", description="Настольная лампа", price=49.99),
        ]
        db.add_all(test_products)
        db.commit()
    db.close()

app.include_router(products.router)
