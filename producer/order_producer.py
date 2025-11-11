from kafka import KafkaProducer
import json
import time
import random
from faker import Faker

fake = Faker()

ORDER_EVENTS = [
    "order_created",
    "payment_done",
    "order_packed",
    "shipped",
    "delivered",
    "cancelled"
]

def get_order_event():
    """Generate a simulated order event"""
    order_id = random.randint(1000, 9999)
    user_id = random.randint(1, 100)
    product = fake.word()
    event = random.choice(ORDER_EVENTS)
    timestamp = int(time.time())

    order_event = {
        "order_id": order_id,
        "user_id": user_id,
        "product": product,
        "event_type": event,
        "timestamp": timestamp
    }
    return order_event


def main():
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    topic_name = "order-events"

    print("🚀 Starting Order Producer...")

    try:
        while True:
            event = get_order_event()
            producer.send(topic_name, value=event)
            print(f"✅ Sent: {event}")
            time.sleep(random.uniform(1, 3))  # random interval
    except KeyboardInterrupt:
        print("\n🛑 Producer stopped.")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
