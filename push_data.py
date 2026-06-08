import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_url = os.getenv("MONGO_DB_URL")

if not mongo_url:
    print("Error: MONGO_DB_URL not found in .env")
    exit()

try:
    print("Fetching CSV file directly from the active GitHub mirror...")
    csv_url = "https://raw.githubusercontent.com/himanshu-yadv/NetworkGuard/main/Network_Data/phisingData.csv"
    df = pd.read_csv(csv_url)
    
    records = df.to_dict(orient="records")
    
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(mongo_url)
    
    database = client["NetworkData"]
    collection = database["NetworkStore"]
    
    print(f"Pushing {len(records)} records to the cloud. This might take a minute...")
    collection.insert_many(records)
    
    print(f"Successfully inserted {len(records)} records into MongoDB!")

except Exception as e:
    print(f"An error occurred: {e}")