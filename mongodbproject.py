import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read environment variables for MongoDB connection
mongo_username = os.getenv('MONGO_INITDB_ROOT_USERNAME', 'default_user')
mongo_password = os.getenv('MONGO_INITDB_ROOT_PASSWORD', 'default_password')
mongo_host = 'mongodb'
mongo_port = 27017

logging.info("Starting data migration process...")

# Load the dataset
logging.info("Loading healthcare dataset from CSV...")
healthcare = pd.read_csv("healthcare_dataset.csv")

# Pre-migration data integrity checks
logging.info("Checking for duplicates in the dataset...")
duplicates_count = healthcare.duplicated().sum()
logging.info(f"Found {duplicates_count} duplicate rows.")
healthcare = healthcare.drop_duplicates()

logging.info("Converting date columns to datetime format...")
healthcare['Date of Admission'] = pd.to_datetime(healthcare['Date of Admission'], errors='coerce')
healthcare['Discharge Date'] = pd.to_datetime(healthcare['Discharge Date'], errors='coerce')

logging.info("Normalizing the 'Name' column...")
healthcare['Name'] = healthcare['Name'].str.title()

logging.info("Checking for invalid date entries...")
invalid_dates = healthcare[healthcare['Discharge Date'] <= healthcare['Date of Admission']]
logging.info(f"Found {len(invalid_dates)} rows with invalid date entries.")

# Connect to MongoDB
logging.info("Connecting to MongoDB...")
try:
    connection_string = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin"
    client = MongoClient(connection_string)
    db = client['healthcare']
    collection = db['patients']
    logging.info("Connected to MongoDB successfully.")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    exit(1)

# Convert DataFrame to dictionary and migrate data
logging.info("Converting DataFrame to dictionary format...")
healthcare_dict = healthcare.to_dict(orient='records')
logging.info(f"Ready to insert {len(healthcare_dict)} records into MongoDB.")

if healthcare_dict:
    try:
        logging.info("Inserting data into MongoDB...")
        collection.insert_many(healthcare_dict)
        logging.info("Data inserted successfully.")
    except Exception as e:
        logging.error(f"Data insertion failed: {e}")
        exit(1)

# CRUD Operations
logging.info("Starting CRUD operation examples...")

# Create (Insert)
new_record = {"Name": "John Doe", "Date of Admission": "2024-01-01", "Discharge Date": "2024-01-05"}
collection.insert_one(new_record)
logging.info("Inserted a new record.")

# Read (Query)
logging.info("Querying the records...")
queried_record = collection.find_one({"Name": "John Doe"})
logging.info(f"Queried record: {queried_record}")

# Update (Modify)
logging.info("Updating an existing record...")
collection.update_one({"Name": "John Doe"}, {"$set": {"Discharge Date": "2024-01-06"}})
logging.info("Updated the record.")

# Delete (Remove)
logging.info("Deleting a record...")
collection.delete_one({"Name": "John Doe"})
logging.info("Record deleted successfully.")

logging.info("Data migration process completed.")
