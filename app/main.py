from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import products, orders, analytics

app = FastAPI(
    title="E-commerce Data Pipeline API",
    description="Python FastAPI + MongoDB data pipeline for products and orders with analytics.",
    version="1.0.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://python-frontend-iota.vercel.app",  # Production frontend
        "http://localhost:5173",                     # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "E-commerce Data Pipeline API is running"}
