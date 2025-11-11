from kafka import KafkaConsumer
import json
from collections import defaultdict
import time

TOPIC_NAME = "order-events"
BOOTSTRAP_SERVERS = ["localhost:9092"]

# Dictionary to store latest status of each order
order_states = defaultdict(lambda: {"user_id": None, "product": None, "last_event": None, "last_updated": None})

def update_order_state(event):
    order_id = event["order_id"]
    order_states[order_id].update({
        "user_id": event["user_id"],
        "product": event["product"],
        "last_event": event["event_type"],
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event["timestamp"]))
    })


def main():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="order-stateful-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("🚀 Listening to Kafka topic:", TOPIC_NAME)

    try:
        for message in consumer:
            event = message.value
            update_order_state(event)

            print(f"🧠 Updated Order {event['order_id']}: {order_states[event['order_id']]}")
            print("-" * 60)

    except KeyboardInterrupt:
        print("\n🛑 Consumer stopped.")
        print("\n📊 Final Order States Snapshot:")
        for order_id, state in order_states.items():
            print(f"{order_id} → {state}")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()
