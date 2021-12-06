# FastAPI Setup

This is my approach to setting up FastAPI for deploying on a docker container setup. I will be using SQLAlchemy and PostgreSQL for the database portion. Here are the pieces to building the API:

1. .env
2. requirements.txt
3. Dockerfile
4. docker-compose.yml
5. app/db.py
6. app/schema.py
7. app/models.py
8. app/main.py

For this document, I will be creating a "People API" where you can perform CRUD operations on a PostgreSQL database for people. People will have the following properties:

```
Name: String
Age: Int
```

### 1. .env
This project requires a `.env` file to properly run. It is used for configuring the `PostgreSQL` container and `db.py` correctly setting up the URL for making the connection. The defaults can be found in `example.env` and should be copied to `.env` for production.

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
POSTGRES_PORT=5432

DOCKER_API_NAME=f_api
DOCKER_DB_NAME=f_db
```


### 2. requirements.txt
At minimum, we will need to require `fastapi` and `uvicorn` for serving the API. We will also be using `sqlalchemy` and `databases[postgresql]` for implementing our database.

Depending on the context of our project, we may need to pull from some Data Science packages. `numpy`, `pandas`, and `sklearn` are my go-to for Machine Learning. I am debating whether I want to use `tensorflow` or `fastai` for Deep Learning. I am interested in `fastai` but I won't rule out `tensorflow` since it is widely used in production.

```
fastapi
uvicorn
SQLAlchemy
databases[postgresql]
```

### 3. Dockerfile
We will pull from a specific `python` image then install our libraries through `requirements.txt`. Finally, we will run `uvicorn` to start the API server.

```dockerfile
FROM python:3.8
COPY ./requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### 4. docker-compose.yml
I use docker-compose for my local setups, but I will look into how to use it for production releases as well. This compose setup creates two containers on a networks: `API` and `Database`.  I'll be setting these containers up with `f_` as a prefix, making `f_api` and `f_db`.

```yaml
version: '3.9'
services:
  f_api:
    container_name: "${DOCKER_API_NAME}"
    build: .
    ports: 
      - "80:80"
    volumes:
      - "./app:/app"
    environment:
      POSTGRES_USER: "${POSTGRES_USER}"
      POSTGRES_PASSWORD: "${POSTGRES_PASSWORD}"
      POSTGRES_DB: "${POSTGRES_DB}"
      POSTGRES_PORT: "${POSTGRES_PORT}"

  f_db:
    container_name: "${DOCKER_DB_NAME}"
    image: postgres:14.1
    restart: always
    environment:
      POSTGRES_USER: "${POSTGRES_USER}"
      POSTGRES_PASSWORD: "${POSTGRES_PASSWORD}"
      POSTGRES_DB: "${POSTGRES_DB}"
```

### 5. app/db.py

This file is responsible for creating our engine instance and connecting to our DB. 

##### PostgreSQL
```python
from os import getenv

import databases
import sqlalchemy

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_PORT = getenv("POSTGRES_PORT")

DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@f_db:{POSTGRES_PORT}/{POSTGRES_DB}'

db = databases.Database(DB_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DB_URL)
```

### 6. app/schema.db

Here we will define our tables using `SQLAlchemy`. 

`(!) Important:` We must include the metadata object from our initialized database.

```python
from sqlalchemy import Table, Column, String, Integer
from .db import metadata

people = Table(
    "people",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("age", Integer)
)
```



### 7. app/models.db

Create our pydantic model for `Person`. Note, we must create both a `PersonIn` and `Person` model for representing when we are going to create into and read from the `people` table, respectively.

```python
from pydantic import BaseModel

PersonIn(BaseModel):
    name: str
    age: int
    
Person(BaseModel):
    id: int
    name: str
    age: int
```



### 8. app/main.py

```python
from fastapi import FastAPI
from typing import List

from .db import db, engine
from .model import Person, PersonIn
from .schema import people

app = FastAPI()

@app.on_event("startup")
async def startup():
    metadata.create_all(engine)
    await db.connect()
    
@app.on_event("shutdown")
async def shutdown()
    await db.disconnect()
    
@app.get("/people/", response_model=List[Person])   
async def read_people():
    query = people.select()
    return await db.fetch_all(query)

@app.post("/people/", response_model=Person)
async def create_person(person: PersonIn):
    query = people.insert().values(name=person.name, age=person.age)
    last_record_id = await db.execute(query)
    return {**person.dict(), "id": last_record_id}

```

