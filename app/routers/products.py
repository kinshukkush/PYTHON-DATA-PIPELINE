from typing import List
from fastapi import APIRouter, HTTPException
from ..models import ProductIn, ProductOut
from ..db import products_collection
from ..services.cleaning import clean_product
from bson import ObjectId

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/bulk-ingest", response_model=List[ProductOut])
def bulk_ingest_products(products: List[ProductIn]):
    cleaned = [clean_product(p.dict()) for p in products]

    # Insert many
    result = products_collection.insert_many(cleaned)
    inserted_ids = result.inserted_ids

    response = []
    for doc_id, product in zip(inserted_ids, cleaned):
        response.append(ProductOut(id=str(doc_id), **product))
    return response


@router.get("/", response_model=List[ProductOut])
def list_products(limit: int = 50):
    docs = list(products_collection.find().limit(limit))
    return [
        ProductOut(
            id=str(doc["_id"]),
            sku=doc["sku"],
            name=doc["name"],
            category=doc.get("category"),
            price=doc["price"],
            currency=doc["currency"],
            in_stock=doc["in_stock"]
        )
        for doc in docs
    ]


@router.get("/{sku}", response_model=ProductOut)
def get_product_by_sku(sku: str):
    doc = products_collection.find_one({"sku": sku})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut(
        id=str(doc["_id"]),
        sku=doc["sku"],
        name=doc["name"],
        category=doc.get("category"),
        price=doc["price"],
        currency=doc["currency"],
        in_stock=doc["in_stock"]
    )
