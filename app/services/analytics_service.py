from typing import Dict, Any, List
import pandas as pd
from ..db import orders_collection
from ..models import AnalyticsSummary, RevenueByDate, TopProduct


def get_analytics_summary() -> AnalyticsSummary:
    orders_cursor = orders_collection.find({})
    orders_list: List[Dict[str, Any]] = list(orders_cursor)

    if not orders_list:
        return AnalyticsSummary(
            total_orders=0,
            total_revenue=0.0,
            revenue_by_date=[],
            top_products=[]
        )

    # Convert to DataFrame
    df_orders = pd.DataFrame(orders_list)

    # Total orders & revenue
    total_orders = len(df_orders)
    total_revenue = float(df_orders["total_amount"].sum())

    # Revenue by date
    df_orders["created_at"] = pd.to_datetime(df_orders["created_at"])
    df_orders["date"] = df_orders["created_at"].dt.date
    revenue_by_date_df = df_orders.groupby("date")["total_amount"].sum().reset_index()

    revenue_by_date = [
        RevenueByDate(
            date=row["date"].isoformat(),
            total_revenue=float(row["total_amount"])
        )
        for _, row in revenue_by_date_df.iterrows()
    ]

    # Explode items to compute top products
    # Each order has "items": [{"sku": ..., "quantity": ...}, ...]
    exploded_rows = []
    for order in orders_list:
        for item in order.get("items", []):
            exploded_rows.append({
                "sku": item["sku"],
                "quantity": item["quantity"],
                "order_total": order["total_amount"]
            })

    if exploded_rows:
        df_items = pd.DataFrame(exploded_rows)
        top_products_df = (
            df_items
            .groupby("sku")
            .agg(
                total_quantity=("quantity", "sum"),
                total_revenue=("order_total", "sum")
            )
            .reset_index()
            .sort_values(by="total_revenue", ascending=False)
            .head(10)
        )

        top_products = [
            TopProduct(
                sku=row["sku"],
                total_quantity=int(row["total_quantity"]),
                total_revenue=float(row["total_revenue"])
            )
            for _, row in top_products_df.iterrows()
        ]
    else:
        top_products = []

    return AnalyticsSummary(
        total_orders=total_orders,
        total_revenue=total_revenue,
        revenue_by_date=revenue_by_date,
        top_products=top_products
    )
