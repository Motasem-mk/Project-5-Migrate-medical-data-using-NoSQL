# **Healthcare Data Migration to MongoDB**

A simple Docker-based solution to migrate CSV healthcare data to MongoDB with validation and CRUD operations.

---

##  **Quick Start**

### **Prerequisites**
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### **Run in 3 Steps**
```bash
# 1. Clone and enter the project
git clone https://github.com/Motasem-mk/project5-MongoDB.git
cd project5-MongoDB

# 2. Set up credentials (edit with your values)
cp .env.example .env

# 3. Start the pipeline
docker-compose up
```

---

## **Project Structure**
```
├── Dockerfile               # Python environment setup
├── docker-compose.yml       # MongoDB + migration service
├── healthcare_dataset.csv   # Sample dataset
├── mongodbproject.py        # Migration/CRUD logic
├── requirements.txt         # Python dependencies
├── .env.example             # Credentials template
├── .gitignore               # Files to ignore in the repository
└── README.md                # This documentation
```

---

## **Environment Variables**

- Configure MongoDB credentials in the `.env` file:
```
MONGO_INITDB_ROOT_USERNAME=your_username
MONGO_INITDB_ROOT_PASSWORD=your_password
```

- Example `.env.example` file:
```
MONGO_INITDB_ROOT_USERNAME=your_username
MONGO_INITDB_ROOT_PASSWORD=your_password
```

---

## **Steps to Verify Data**

1. Connect to MongoDB using **MongoDB Compass**:
   ```
   mongodb://your_username:your_password@localhost:27017/
   ```

2. Check the `healthcare` database and the `patients` collection to confirm the data migration.

---

## **Docker Configuration**

### **docker-compose.yml**
```yaml
version: '3.9'

services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_INITDB_ROOT_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_INITDB_ROOT_PASSWORD}

  migration:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mongodb-migration
    depends_on:
      - mongodb
    volumes:
      - ./healthcare_dataset.csv:/app/healthcare_dataset.csv

volumes:
  mongodb_data:
```

---

### **Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 27017

CMD ["python", "mongodbproject.py"]
```

---

## **Data Migration Process**

1. **Loading the Data**:
   - The script reads the CSV file (`healthcare_dataset.csv`) using `pandas`.

2. **Data Cleaning**:
   - Removes duplicates and invalid records.
   - Converts date columns to datetime format.
   - Normalizes text fields (e.g., names).

3. **Data Insertion**:
   - The cleaned data is inserted into the `patients` collection in the `healthcare` database.
   - Post-migration checks validate the data integrity.

---

## **Volumes**

1. **mongodb_data**:
   - Persistently stores MongoDB data between container restarts.

2. **CSV Volume**:
   - Mounts the `healthcare_dataset.csv` file inside the container at `/app/healthcare_dataset.csv`.

---

## **CRUD Operations**

### **Create**
```python
new_record = {
    "Name": "Alice Brown",
    "Age": 25,
    "Medical Condition": "Asthma",
    "Date of Admission": "2024-03-01",
    "Discharge Date": "2024-03-05"
}
collection.insert_one(new_record)
```

### **Read**
```python
results = collection.find({"Age": {"$gte": 88}})
```

### **Update**
```python
collection.update_many({"Name": "Alice Brown"}, {"$set": {"Room Number": 203}})
```

### **Delete**
```python
collection.delete_many({"Name": "Alice Brown"})
```

---

## **Dependencies**
Listed in `requirements.txt`:
```
pandas
pymongo
```
Install them using:
```bash
pip install -r requirements.txt
```

---

## **Project Limitations**
- This project focuses on data migration and basic CRUD operations.
- No additional indexes were created apart from the default `_id` index.
- Future improvements could include performance optimizations, such as indexing frequently queried fields. 

---

## **Troubleshooting**

### **1. MongoDB Connection Issues**
   Ensure that:
   - Docker containers are running.
   - MongoDB is exposed on port `27017`.

### **2. Data Issues**
   If data migration fails, ensure the CSV file:
   - Has no missing or invalid fields.
   - Contains valid date formats.

---

## **Contributors**
- Motasem Abualqumboz – Data Engineer Intern at DataSoluTech