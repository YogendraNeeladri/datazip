# MongoDB to Apache Iceberg Data Pipeline

This project demonstrates a data pipeline that extracts data from MongoDB and syncs it to Apache Iceberg using OLake's Hive integration, with querying capabilities via Apache Spark.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- pip (Python package manager)

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the required services using Docker Compose:
```bash
docker-compose up -d
```

3. Wait for all services to be healthy (this may take a few minutes)

## Usage

1. Load sample data into MongoDB:
```bash
python load_sample_data.py
```

2. Sync data from MongoDB to Iceberg:
```bash
python sync_to_iceberg.py
```

## Services

- MongoDB: localhost:27017
- MinIO (S3): 
  - API: localhost:9000
  - Console: localhost:9001 (credentials: minioadmin/minioadmin)
- Hive Metastore: localhost:9083

## Data Model

The sample data consists of orders with the following schema:
- order_id (string)
- customer_id (string)
- customer_name (string)
- customer_email (string)
- product_name (string)
- quantity (integer)
- unit_price (double)
- total_amount (double)
- order_date (timestamp)
- status (string)

## Troubleshooting

1. If services fail to start, try:
```bash
docker-compose down -v
docker-compose up -d
```

2. To check service logs:
```bash
docker-compose logs -f [service_name]
``` 