from fastapi import FastAPI
from .routers import products, orders, analytics

app = FastAPI(
    title="E-commerce Data Pipeline API",
    description="Python FastAPI + MongoDB data pipeline for products and orders with analytics.",
    version="1.0.0",
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "E-commerce Data Pipeline API is running"}
