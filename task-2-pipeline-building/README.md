# Weather Data Pipeline using Open-Meteo API

## Overview

This project demonstrates a complete end-to-end data pipeline built using Python and Google BigQuery.

The pipeline fetches weather forecast data from the Open-Meteo public API, transforms and cleans the data, stores it in BigQuery, and enables SQL-based analysis.

This project was built as part of the Data & AI Product Engineer assessment.

---

# API Chosen

## Open-Meteo API

Website:
https://open-meteo.com/

### Why I Chose This API

I selected Open-Meteo because:
- It is completely free
- No API key is required
- The API provides structured JSON data
- The data includes nested fields suitable for transformation
- It is reliable and easy to test repeatedly

---

# Pipeline Architecture

```text
Open-Meteo API
       ↓
Python Fetch Script
       ↓
Data Transformation using Pandas
       ↓
CSV Export
       ↓
Google BigQuery
       ↓
SQL Analysis
```

---

# Features Implemented

## 1. API Data Fetching

- Connected to Open-Meteo API using Python requests library
- Parameterized latitude and longitude
- Added API error handling

## 2. Data Transformation

- Flattened nested JSON data into tabular format
- Converted datetime values properly
- Handled null values using fillna()
- Added derived analytical field:
  - temperature_category

## 3. Logging

Implemented logging using Python logging module:
- pipeline start
- API success/failure
- transformation status
- BigQuery upload status

## 4. CSV Export

Transformed data is exported to:
data/weather_data.csv

## 5. BigQuery Integration

- Created BigQuery Sandbox project
- Created dataset:
  weather_pipeline
- Uploaded transformed dataframe into BigQuery table:
  weather_data

---

# Project Structure

```text
task-2-pipeline-building/
│
├── data/
│   └── weather_data.csv
│
├── logs/
│   └── pipeline.log
│
├── sql/
│   └── weather_analysis.sql
│
├── src/
│   └── weather_pipeline.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# How to Run the Pipeline

## Step 1

Clone repository

```bash
git clone <repo-url>
```

## Step 2

Create virtual environment

```bash
python -m venv venv
```

## Step 3

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

## Step 4

Install dependencies

```bash
pip install -r requirements.txt
```

## Step 5

Run pipeline

```bash
cd src
python weather_pipeline.py
```

---

# BigQuery Setup

1. Created a Google BigQuery Sandbox project
2. Created dataset:
   weather_pipeline
3. Created service account with BigQuery Admin role
4. Downloaded JSON credentials
5. Connected Python pipeline to BigQuery

---

# SQL Analysis Query

```sql
SELECT
    city,
    temperature_category,
    COUNT(*) AS total_records,
    AVG(temperature) AS average_temperature
FROM
    `tokyo-crane-497603-t5.weather_pipeline.weather_data`
GROUP BY
    city, temperature_category
ORDER BY
    average_temperature DESC;
```

---

# Sample Insight

The SQL query helps identify:
- average temperatures
- weather distribution
- category-wise aggregation

This demonstrates that the stored data is queryable and analytically useful.

---

# Production Considerations

## Scheduling

In production, I would schedule this pipeline using:
- Apache Airflow
OR
- Google Cloud Scheduler

The pipeline could run every 6 hours automatically.

---

## Failure Monitoring

To monitor failures:
- logging system
- retry mechanism
- email/slack alerts
- pipeline monitoring dashboard

---

## Scaling for 10x Data Volume

If the pipeline scaled significantly, I would:
- use partitioned BigQuery tables
- batch API requests
- implement incremental loading
- use orchestration tools like Airflow
- containerize pipeline using Docker

---

# Improvements with More Time

- Add unit tests
- Add Docker support
- Add configuration files
- Add multiple city support
- Add data validation framework
- Add Airflow DAG

---

# Author

Pugal B