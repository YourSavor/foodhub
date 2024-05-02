# CMSC 127 Food Hub

## Description
A FastAPI application with a PostgreSQL database backend.

## Installation

### Step 1: Clone the repo
Clone this repository to your local machine using the following command:

```bash
git clone https://{insert your github code}github.com/YourSavor/foodhub.git
```

### Step 2: Create virtual environment and install dependencies
Navigate to the project directory and create a virtual environment. Then, activate the virtual environment and install the required dependencies using the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Download .env file
Download the .env file containing the required environment variables and paste it in the working directory (same directory as main).

### Usage

To run the FastAPI application, execute the following command:
```bash
python3 -m uvicorn main:app --reload
```

### How It Works
The db.py module provides functions to establish a connection to the PostgreSQL database using the psycopg2 library. It loads the required environment variables from the .env file and utilizes them to connect to the database.

This module also includes a sample_query() function to demonstrate basic database operations like inserting and querying data