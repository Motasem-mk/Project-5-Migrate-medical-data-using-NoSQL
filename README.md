# MongoDB Data Migration Project

This project demonstrates how to set up a MongoDB service with data migration using Docker Compose. The project integrates MongoDB, runs a Python data migration script, loads a healthcare CSV dataset, and performs basic CRUD operations.

## Project Structure

```text
├── data/
│   └── healthcare_dataset.csv
├── mongodbproject.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Docker Compose Configuration

The services are configured in `docker-compose.yml` using Docker Compose.

### 1. MongoDB Service

The MongoDB service uses the official MongoDB image.

```yaml
mongodb:
  image: mongo:6.0
  environment:
    MONGO_INITDB_ROOT_USERNAME: ${MONGO_INITDB_ROOT_USERNAME}
    MONGO_INITDB_ROOT_PASSWORD: ${MONGO_INITDB_ROOT_PASSWORD}
  ports:
    - "27017:27017"
  volumes:
    - mongodb_data:/data/db
```

Main points:

* MongoDB runs on port `27017`.
* MongoDB credentials are loaded from the `.env` file.
* MongoDB data is stored in a Docker volume for persistence.

### 2. MongoDB Migration Service

The migration service builds a Python container and runs the migration script.

```yaml
mongodb-migration:
  build:
    context: .
  environment:
    - MONGO_INITDB_ROOT_USERNAME=${MONGO_INITDB_ROOT_USERNAME}
    - MONGO_INITDB_ROOT_PASSWORD=${MONGO_INITDB_ROOT_PASSWORD}
  depends_on:
    - mongodb
  command: python mongodbproject.py
```

Main points:

* The service runs `mongodbproject.py`.
* It connects to the MongoDB container.
* It loads the healthcare dataset and inserts it into MongoDB.
* It performs post-migration checks and CRUD operations.

## Prerequisites

Before running the project, make sure you have:

* Docker Desktop installed and running.
* Git installed.
* A `.env` file created from `.env.example`.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Motasem-mk/Project-5-Migrate-medical-data-using-NoSQL.git
cd Project-5-Migrate-medical-data-using-NoSQL
```

### 2. Create the `.env` file

```bash
cp .env.example .env
```

Update the `.env` file with your MongoDB credentials:

```env
MONGO_INITDB_ROOT_USERNAME=your_username
MONGO_INITDB_ROOT_PASSWORD=your_password
```

The `.env` file is excluded from GitHub using `.gitignore`.

### 3. Check the dataset path

The dataset is stored in:

```text
data/healthcare_dataset.csv
```

In `mongodbproject.py`, the CSV should be loaded with:

```python
healthcare = pd.read_csv("data/healthcare_dataset.csv")
```

### 4. Build and start the services

```bash
docker-compose up --build
```

This command starts MongoDB and runs the Python migration script.

## Migration Process and CRUD Operations

The migration script `mongodbproject.py` performs the following steps:

### 1. Load the dataset

The script reads the healthcare CSV file using Pandas.

```python
healthcare = pd.read_csv("data/healthcare_dataset.csv")
```

### 2. Clean the data

The script performs basic data preparation:

* checks duplicate rows;
* removes duplicates;
* converts date columns to datetime format;
* normalizes the `Name` column;
* checks invalid date entries.

### 3. Connect to MongoDB

The script connects to MongoDB using credentials stored in environment variables.

```python
connection_string = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin"
```

The database used is:

```text
healthcare
```

The collection used is:

```text
patients
```

### 4. Insert data into MongoDB

The Pandas DataFrame is converted into a list of dictionaries and inserted into MongoDB.

```python
healthcare_dict = healthcare.to_dict(orient="records")
collection.insert_many(healthcare_dict)
```

### 5. Run post-migration checks

The script performs several checks after insertion:

* compares the number of CSV rows with MongoDB documents;
* checks duplicate records in MongoDB;
* validates date consistency;
* searches for a sample record.

### 6. Perform CRUD operations

The script demonstrates basic CRUD operations:

* Create: insert a sample record;
* Read: query the inserted record;
* Update: update the discharge date;
* Delete: delete the sample record.

## Verifying the Data in MongoDB

You can connect to MongoDB using MongoDB Compass or the MongoDB shell.

Connection information:

```text
Host: localhost
Port: 27017
Database: healthcare
Collection: patients
```

Use the username and password defined in your `.env` file.

## Creating the `data_engineer` User in MongoDB

After the MongoDB container is running, you can create a dedicated user for the `healthcare` database.

### 1. Connect to MongoDB as admin

```bash
docker exec -it <mongodb_container_name> mongosh \
  -u <admin_username> \
  -p <admin_password> \
  --authenticationDatabase admin
```

### 2. Switch to the `healthcare` database

```javascript
use healthcare
```

### 3. Create the `data_engineer` user

```javascript
db.createUser({
  user: "data_engineer",
  pwd: "<your_secure_password>",
  roles: [
    { role: "readWrite", db: "healthcare" },
    { role: "dbAdmin", db: "healthcare" }
  ]
})
```

### 4. Verify the user creation

```javascript
show users
```

### 5. Connect as `data_engineer`

```bash
docker exec -it <mongodb_container_name> mongosh \
  -u data_engineer \
  -p <your_secure_password> \
  --authenticationDatabase healthcare
```

## Main Technologies

* MongoDB
* Docker
* Docker Compose
* Python
* Pandas
* PyMongo
* python-dotenv

## Notes

* The `.env` file must not be pushed to GitHub.
* Real passwords should never be written in the README.
* The dataset is stored inside the `data/` folder.
* The Python script must use the correct dataset path: `data/healthcare_dataset.csv`.

## Author

Motasem Abualqumboz

OpenClassrooms Data Engineer Path
