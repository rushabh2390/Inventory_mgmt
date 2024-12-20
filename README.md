### How to run this.
---   
1. Set up .env file with following keys. You can set values as per your requirement
````
SECRET_KEY=FBnvkjzqjWqJfXJs
MONGO_URI=mongodb://localhost:27017/
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/inventory_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_NAME=inventory_db
DATABASE_PORT=5432
BROKER_ADDRESS=localhost:9092
````
2. Install dependenceny   
````
pip install -r requirements.txt
````
3. Install and run Kafka and kafka UI using docker_compose file. You can also install locally from here [Kafka](https://kafka.apache.org/downloads). [Kafka-ui](https://github.com/provectus/kafka-ui).
````
docker-compose up -d
````
4. once Kafka install and running run the below command to start fastapi
````
uvicorn main:app --reload
````
5. You can see api swagger here [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
6. You can see Kafka dashborad here [http://localhost:8080/](http://localhost:8080/).
---
## Using Docker
1. Run below command.   
````
docker-compose up -d
````
2. You can see api swagger here [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. You can see Kafka dashborad here [http://localhost:8080/](http://localhost:8080/).
