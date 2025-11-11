# consumer/api_server.py
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="Order Tracking API", version="1.0")

DB_CONFIG = {
    "host": "localhost",
    "database": "orders_db",
    "user": "admin",
    "password": "admin123"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.get("/")
def root():
    return {"message": "✅ Order Tracking API is running!"}

@app.get("/orders")
def get_all_orders():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM orders ORDER BY updated_at DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"orders": rows}

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM orders WHERE order_id = %s;", (order_id,))
    order = cur.fetchone()
    cur.close()
    conn.close()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
