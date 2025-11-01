# 🧠 Stock Trading ETL Pipeline (Python + Snowflake)
## 📘 Overview

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline using Python to pull real-time stock ticker data from the Polygon.io API and load it into Snowflake for data analysis and warehousing.
The goal was to build a beginner-friendly, production-like data engineering workflow — fully automated and scalable.

## ⚙️ Tech Stack

Python – Core language for data extraction and transformation

Polygon.io API – Source of stock market data

Snowflake – Cloud data warehouse for storing processed data

dotenv – Secure management of API keys and credentials

Git + GitHub – Version control and project collaboration

## 🏗️ Project Structure
stock-trading-python-app/
│
├── script.py

├── scheduler.py

├── requirements.txt

├── Dockerfile

├── .dockerignore

├── .env

├── .gitignore

├── tickers.csv

├── pythonenv/

└── README.md


## 📂 File Descriptions

### script.py

The main ETL script.

Connects to the Polygon.io API, fetches stock ticker data, transforms it, and loads it into your Snowflake database.

Includes progress logs like “Inserted 44034/44034 records…” after loading completion.

### scheduler.py

Automates and schedules the ETL process.

Useful for running the pipeline periodically (e.g., daily updates).

### requirements.txt

Lists Python dependencies such as snowflake-connector-python, requests, and python-dotenv.

Run pip install -r requirements.txt to install all dependencies.

### .env

Contains sensitive credentials like API keys and Snowflake login details.

Managed securely using the dotenv package to avoid hardcoding secrets.

### tickers.csv

Local CSV backup of fetched ticker data.

Helps with debugging, offline analysis, or testing data transformations.

### .gitignore

Tells Git which files/folders to exclude (e.g., .env, pythonenv/).

Keeps your repo clean and prevents credential leaks.

### pythonenv/

Local virtual environment folder containing project-specific dependencies.

Should not be uploaded to GitHub — it’s ignored by .gitignore.

### .dockerignore

Specifies which files and folders Docker should ignore when building the image (e.g., .env, pythonenv/,

## 🚀 How to Run

### Clone the repository

```
git clone https://github.com/Duncan610/stock-trading-python-app.git
cd stock-trading-python-app
```

### Set up a virtual environment

```
python3 -m venv pythonenv
source pythonenv/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```

Create a .env file with your credentials:

```
POLYGON_API_KEY=your_api_key
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=STOCKS_DB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_TABLE=TICKERS
```

Run the ETL script

```
python3 script.py
```

## 💡 Highlights

Extracted over 44,000+ stock tickers from the Polygon.io API.

Built a scalable ETL pipeline that loads data into Snowflake seamlessly.

Implemented secure credential management using .env.

Practiced real-world data engineering concepts such as batching and incremental loads.
