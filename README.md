# E-commerce Data Pipeline API (Python + FastAPI + MongoDB)

This project implements a small data pipeline for an e-commerce system using **Python**, **FastAPI**, and **MongoDB**.

It exposes APIs to ingest **product** and **order** data, applies basic **data cleaning and validation**, stores the records in MongoDB, and provides **analytics endpoints** (total revenue, revenue by date, top products).

## Tech Stack

- Python
- FastAPI
- MongoDB (via `pymongo`)
- Pydantic (validation)
- Pandas (analytics)
- Uvicorn (ASGI server)

## Features

- Bulk ingestion of products: `POST /products/bulk-ingest`
- Bulk ingestion of orders: `POST /orders/bulk-ingest`
- List products: `GET /products`
- List orders: `GET /orders`
- Basic analytics summary:
  - total orders
  - total revenue
  - revenue by date
  - top products (by revenue)

## Project Structure

- `app/`
  - `main.py` – FastAPI application entrypoint
  - `config.py` – environment configuration
  - `db.py` – MongoDB client and collections
  - `models.py` – Pydantic models (schemas)
  - `services/` – business logic
  - `routers/` – API routers (products, orders, analytics)
- `scripts/`
  - `load_sample_data.py` – ETL script to load sample JSON data into MongoDB
- `data/` – sample JSON data files

## Setup

```bash
git clone <your-repo-url>
cd ecommerce-data-pipeline-api

python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
