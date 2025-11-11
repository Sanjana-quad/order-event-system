# 🛍️ Order Event Processing System (E-commerce Domain)
### 🎯 Goal
- Simulate e-commerce order lifecycle events → stream them via Apache Kafka → process updates in real time → persist to PostgreSQL → expose analytics via FastAPI + Grafana.

### 🧩 Project Overview

~ This project demonstrates a real-time event-driven architecture used in large-scale e-commerce systems.
~ It captures simulated order events (like order_created, payment_done, shipped, delivered) from a Kafka producer, processes them through a consumer, updates PostgreSQL, and exposes live analytics via a FastAPI REST API and /metrics endpoint for Grafana monitoring.

### ⚙️ Tech Stack
| Component | Technology |
| Programming Language | Python |
| Message Broker | Apache Kafka (Docker Compose) |
| Database | PostgreSQL |
| Backend API | FastAPI |
| Monitoring | Prometheus + Grafana |
| Containerization | Docker Compose |
| Streaming Library | kafka-python |

### 📁 Project Structure
order-event-system/
- docker-compose.yml         # Kafka, Zookeeper, Postgres, FastAPI, Prometheus stack
- producer/
-- order_producer.py      # Simulates real-time order lifecycle events
- consumer/
-- order_consumer.py      # Processes events, updates order state in DB
- api/
-- api_server.py          # FastAPI server exposing /orders and /metrics endpoints
- database/
-- db_init.py             # PostgreSQL schema creation
- logs/
-- consumer.log           # Real-time consumer activity logs
- requirements.txt
- README.md

## 🚀 Milestone 1 — Kafka Setup
### Step 1. Start Kafka Cluster
    ```bash
    docker-compose up -d

Verify containers:
    ```bash
    docker ps

## ⚙️ Milestone 2 — Order Producer

Simulates the order lifecycle using KafkaProducer:
    ```json
    {
    "order_id": "12345",
    "user_id": 1001,
    "status": "payment_done",
    "timestamp": 1730880000
    }


Run:
    ```bash
    python producer/order_producer.py


✅ You’ll see live order events being sent to Kafka.

## 🧠 Milestone 3 — Consumer (Order Processor)

Consumes events from order-events topic and updates state in memory (and later DB).
Two modes were tested:

Stateless: just prints messages (for debugging)

Stateful (final): maintains latest order state per order_id and persists to DB.

Run:
    ```bash
    python consumer/order_consumer.py

## 💾 Milestone 4 — PostgreSQL Integration

Your consumer now writes each order’s latest state to PostgreSQL.

Start DB in Docker:
    ```bash
    docker-compose up -d postgres


View table contents:
    ```bash
    docker exec -it postgres psql -U postgres -d orders_db
    SELECT * FROM orders;

## 🌐 Milestone 5 — FastAPI REST API

Start the API server:
    ```bash
    uvicorn api.api_server:app --reload --port 8000

| Available Endpoints:  |
| Endpoint | Method | Description |
| /orders | GET | Retrieve all orders |
| /orders/{order_id} | GET | Retrieve details of a specific order |