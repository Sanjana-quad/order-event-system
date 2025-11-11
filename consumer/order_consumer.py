from kafka import KafkaConsumer
import json
import time
from collections import defaultdict
from db import init_db, upsert_order

# --- Kafka & Topic Setup ---
TOPIC_NAME = "order-events"
BOOTSTRAP_SERVERS = ["localhost:9092"]

# --- Initialize DB ---
init_db()

# --- In-Memory State Tracking ---
order_states = defaultdict(lambda: {
    "user_id": None,
    "product": None,
    "status": None,
    "last_event": None,
    "last_updated": None
})

def update_order_state(event):
    order_id = event["order_id"]
    order_states[order_id].update({
        "user_id": event.get("user_id"),
        "product": event.get("product"),
        "status": event.get("status"),
        "last_event": event.get("event_type"),
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event["timestamp"]))
    })

def print_order_snapshot(order_id):
    """Print a single order’s latest state (for visibility)."""
    print(f"🧠 Order {order_id} State: {order_states[order_id]}")
    print("-" * 60)

def main():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="order-stateful-processor",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("📦 Order Consumer started... Listening for events...")

    try:
        for msg in consumer:
            event = msg.value
            order_id = event["order_id"]

            # --- Update in-memory state ---
            update_order_state(event)

            # --- Persist to database ---
            upsert_order(event)

            # --- Log live update ---
            print(f"✅ Updated order {order_id} → {event.get('status', event.get('event_type', 'UNKNOWN'))}")
            print_order_snapshot(order_id)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n🛑 Consumer stopped.")
        print("\n📊 Final Order States Snapshot:")
        for order_id, state in order_states.items():
            print(f"{order_id} → {state}")

    finally:
        consumer.close()

if __name__ == "__main__":
    main()
