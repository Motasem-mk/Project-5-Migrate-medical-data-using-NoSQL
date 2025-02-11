# MongoDB Data Migration Project

This project demonstrates how to set up a MongoDB service with data migration using Docker Compose. The project involves integrating MongoDB, running data migration scripts, and performing basic CRUD operations.

## Project Structure

```
├── data/
│   └── healthcare_dataset.csv  # CSV file moved to the 'data' folder
├── mongodbproject.py           # Python script for migration and CRUD operations
├── Dockerfile                  # Dockerfile to build the migration container
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies file
├── README.md                   # Project documentation
├── .env.example                # Template for environment variables (shared in repo)
├── .env                        # Actual environment variables (excluded from repo)
└── .gitignore                  # Specifies files and folders to ignore in version control

```

---

## Docker Compose Configuration

### `docker-compose.yml`
The services are configured in `docker-compose.yml` using Docker's **default network**. Here’s a breakdown of the services:

### **1. MongoDB Service**
```yaml
services:
  mongodb:
    image: mongo:6.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_INITDB_ROOT_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_INITDB_ROOT_PASSWORD}
    ports:
      - "27017:27017"
```
- **Environment Variables:** MongoDB root credentials are passed through environment variables.
- **Ports:** The database is accessible on port `27017`.
- **Network:** Docker's default network is used for communication between services.

---

### **2. MongoDB Migration Service**
```yaml
services:
  mongodb-migration:
    build:
      context: .
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_INITDB_ROOT_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_INITDB_ROOT_PASSWORD}
    depends_on:
      - mongodb
    volumes:
      - .:/app
    command: python mongodbproject.py
```
- **Build:** The migration service is built from the local context (`.`).
- **Volumes:** 
  - The project directory (`.`) is mounted to `/app` in the container to allow access to local files.
- **Role:** The migration service performs operations as a **root** user inside the container.
- **Command:** Executes the Python script (`mongodbproject.py`).

---

## Prerequisites

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop) and ensure it is running.
2. Clone the repository to your local machine:
   ```sh
   git clone <repository-url>
   ```
3. Navigate to the project directory:
   ```sh
   cd <project-directory>
   ```

---

## Setup Instructions

1. Create a `.env` file by copying `.env.example`:
   ```sh
   cp .env.example .env
   ```
   Update the `.env` file with your MongoDB root username and password.

2. Build and start the services:
   ```sh
   docker-compose up --build
   ```

3. Verify the setup:
   - MongoDB should be running on port `27017`.
   - The migration service will load the CSV data, perform migrations, and execute CRUD operations.

---

## Migration Process and CRUD Operations

The migration script (`mongodbproject.py`) follows these steps:

1. **Data Migration**  
   - The script reads data from `healthcare_data.csv`.
   - Duplicate entries are removed, date formats are normalized, and the cleaned data is inserted into MongoDB.

2. **CRUD Operations**
   - Insert a sample record into the `patients` collection.
   - Query and display a sample record.
   - Update an existing record.
   - Delete a record and confirm the deletion.

---

## Verifying the Data in MongoDB

You can connect to MongoDB using [MongoDB Compass](https://www.mongodb.com/products/compass) or any MongoDB client with the following details:
- **Host:** `localhost`
- **Port:** `27017`
- **Username:** Your MongoDB root username (from `.env`)
- **Password:** Your MongoDB root password (from `.env`)

---

## Customization

Feel free to modify the following files based on your project requirements:
- `mongodbproject.py` for data transformation logic.
- `docker-compose.yml` for service configuration.
- `requirements.txt` to add or remove Python dependencies.

---

## Contributing

Contributions are welcome! Fork the repository, make your changes, and create a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

