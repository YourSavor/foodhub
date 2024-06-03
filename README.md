# YourSavor : CMSC 127 Food Hub

## Developers
- Axel Balitaan
- Adrian Carl Cutines
- Franz Christian Morelos

## Description
A FastAPI application with a PostgreSQL database backend designed for a food review recording system. Users can add their own establishments and food items, and review both establishments and individual food items.

## Installation

#### Step 1: Clone the repo
Clone this repository to your local machine using the following command:

```bash
git clone https://<insert your github code>github.com/YourSavor/foodhub.git
```

#### Step 2: Create virtual environment and install dependencies
Navigate to the project directory and create a virtual environment. Then, activate the virtual environment and install the required dependencies using the following commands:

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

#### Step 3: Download .env file
Download the .env file containing the required environment variables and paste it in the working directory (same directory as main).

## Usage

To run the FastAPI application, execute the following commands:

#### Backend

```bash
On the main directory:
    source .venv/bin/activate
On dir/api:
    python3 -m uvicorn main:app --reload
```    
    
#### Frontend
```
On the main directory:
    source .venv/bin/activate
On dir/web:
    streamlit run app.py
```