# consumer/db.py
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="orders_db",
        user="admin",
        password="admin123"
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id VARCHAR(50) PRIMARY KEY,
            user_id INT,
            status VARCHAR(50),
            total_amount FLOAT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def upsert_order(order):
    conn = get_connection()
    cur = conn.cursor()

    status = order.get("status", order.get("event_type","UNKNOWN"))
    amount = order.get("total_amount", 0)

    cur.execute("""
        INSERT INTO orders (order_id, user_id, status, total_amount)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (order_id)
        DO UPDATE SET
            status = EXCLUDED.status,
            total_amount = EXCLUDED.total_amount,
            updated_at = CURRENT_TIMESTAMP;
    """, (order["order_id"], order["user_id"], status, amount))
    conn.commit()
    cur.close()
    conn.close()
