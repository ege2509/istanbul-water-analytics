
# Istanbul Water Analytics

An end-to-end data engineering project that tracks and analyzes Istanbul's dam levels, precipitation, and daily water consumption across 10 major dams from 2011 to 2024.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Data Sources](#data-sources)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Pipeline](#pipeline)
- [Database Schema](#database-schema)
- [Derived Metrics & Views](#derived-metrics--views)
- [Technologies](#technologies)

---

## Overview

Istanbul relies on 10 major dams for its water supply. This project ingests raw dam occupancy, precipitation, and city consumption data, cleans and transforms it, loads it into a PostgreSQL database, and derives key metrics such as rolling averages and estimated days of water supply remaining.

The goal is to provide a reliable, queryable foundation for monitoring Istanbul's water situation over time.

The data used for this project are from 2011 to 2024

---

## Architecture

```
Raw Excel Data
      │
      ▼
┌─────────────┐
│   Cleaning  │  clean_datasets.py
│  (pandas)   │
└─────┬───────┘
      │  Cleaned Excel files
      ▼
┌─────────────┐
│  Ingestion  │  ingestion.py
│  (psycopg2) │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ PostgreSQL  │  schema.sql
│  Database   │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│  Validation │  validation.py
└─────┬───────┘
      │
      ▼
┌─────────────┐
│SQL Views &  │  Derived metrics
│  Metrics    │  (rolling avgs, days of supply)
└─────────────┘
```

---

## Data Sources

| Source | Description | Columns |
|--------|-------------|---------|
| Precipitation data | Daily precipitation per dam (%) | Date, dam-wise precipitation percentages |
| Occupancy data | Daily occupancy per dam (%) | Date, dam-wise occupancy percentages |
| Consumption data | Istanbul's daily water consumption (m³) | Date, daily consumption in cubic meters |

---

## Project Structure

```
istanbul-water-analytics/
│
├── data/                          # Raw and processed data files
│
├── sql/                           # SQL scripts
│   └── schema.sql                 # Database schema and view definitions
│
├── transformation/                # Transformation and metrics scripts
│   └── daily_total_metrics.py     # Derived metrics calculations
│
├── clean_datasets.py              # Data cleaning (pandas)
├── ingestion.py                   # ETL: load cleaned data into PostgreSQL
├── validation.py                  # Data validation checks
├── trends.py                      # Trend analysis
│
└── README.md                      # This file
```

---

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 14+

### 1. Clone the repository

```bash
git clone https://github.com/ege2509/istanbul-water-analytics.git
cd istanbul-water-analytics
```

### 2. Install dependencies

```bash
pip install pandas psycopg2-binary openpyxl python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```
DB_NAME=istanbul-water-analytics
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Create the database

```bash
psql -U postgres -c "CREATE DATABASE istanbul-water-analytics;"
psql -U postgres -d istanbul-water-analytics -f sql/schema.sql
```

---

## Pipeline

Run the scripts in this order:

```bash
# 1. Clean the raw data
python clean_datasets.py

# 2. Ingest cleaned data into PostgreSQL
python ingestion.py

# 3. Validate the loaded data
python validation.py
```

---

## Database Schema

### Tables

| Table | Description |
|-------|-------------|
| `dams` | Stores the 10 dams and their max capacities (m³) |
| `daily_dam` | Daily precipitation and occupancy per dam (m³ and %) |
| `city_consumption` | Istanbul's daily water consumption (m³) |
| `daily_system_metrics` | Daily precipitation and occupancy stats for all dams combined |


### Dams Tracked

| Dam Name | Max Capacity (m³) |
|----------|-------------------|
| Ömerli | 235,371,000 |
| Terkos | 162,241,000 |
| Büyükçekmece | 148,943,000 |
| Darlık | 107,500,000 |
| Sazlıdere | 88,730,000 |
| Pabuçdere | 58,500,000 |
| Alibey | 34,143,000 |
| Kazandere | 17,424,000 |
| Elmalı | 9,600,000 |
| İstrancalar | 6,231,000 |

---

## Derived Metrics & Views

### `dam_rolling_averages`

Calculates 7-day, 30-day, and 90-day rolling averages for both precipitation and occupancy per dam using window functions.

| Column | Description |
|--------|-------------|
| `precipitation_7day_avg` | 7-day rolling average of precipitation (m³) |
| `precipitation_30day_avg` | 30-day rolling average of precipitation (m³) |
| `precipitation_90day_avg` | 90-day rolling average of precipitation (m³) |
| `occupancy_7day_avg` | 7-day rolling average of occupancy (m³) |
| `occupancy_30day_avg` | 30-day rolling average of occupancy (m³) |
| `occupancy_90day_avg` | 90-day rolling average of occupancy (m³) |

### `consumption_averages`

Calculates 7-day, 30-day, and 90-day rolling averages for Istanbul's daily water consumption.

| Column | Description |
|--------|-------------|
| `consumption_7day_avg` | 7-day rolling average of consumption (m³) |
| `consumption_30day_avg` | 30-day rolling average of consumption (m³) |
| `consumption_90day_avg` | 90-day rolling average of consumption (m³) |

### `days_of_supply`

Estimates how many days of water remain based on current dam occupancy and recent consumption rate.

```
days_of_supply = occupancy_m3 / consumption_30day_avg
```

> Note: This is a worst-case estimate — it does not account for future precipitation that could refill the dams.

---

## Technologies

| Tool | Purpose |
|------|---------|
| Python | Data cleaning, ingestion, validation |
| pandas | Data manipulation and transformation |
| psycopg2 | PostgreSQL connection and batch inserts |
| PostgreSQL | Data storage and SQL views |
| python-dotenv | Secure credential management |