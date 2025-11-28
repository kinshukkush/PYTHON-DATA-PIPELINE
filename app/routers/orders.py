from typing import List
from fastapi import APIRouter, HTTPException
from ..models import OrderIn, OrderOut
from ..db import orders_collection
from ..services.cleaning import clean_order

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/bulk-ingest", response_model=List[OrderOut])
def bulk_ingest_orders(orders: List[OrderIn]):
    cleaned = [clean_order(o.dict()) for o in orders]
    result = orders_collection.insert_many(cleaned)
    inserted_ids = result.inserted_ids

    response = []
    for doc_id, order in zip(inserted_ids, cleaned):
        response.append(OrderOut(id=str(doc_id), **order))
    return response


@router.get("/", response_model=List[OrderOut])
def list_orders(limit: int = 50):
    docs = list(orders_collection.find().limit(limit))
    return [
        OrderOut(
            id=str(doc["_id"]),
            order_id=doc["order_id"],
            user_id=doc["user_id"],
            items=doc["items"],
            total_amount=doc["total_amount"],
            currency=doc["currency"],
            created_at=doc["created_at"]
        )
        for doc in docs
    ]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: str):
    doc = orders_collection.find_one({"order_id": order_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderOut(
        id=str(doc["_id"]),
        order_id=doc["order_id"],
        user_id=doc["user_id"],
        items=doc["items"],
        total_amount=doc["total_amount"],
        currency=doc["currency"],
        created_at=doc["created_at"]
    )
