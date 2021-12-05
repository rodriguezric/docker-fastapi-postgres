from fastapi import FastAPI
from typing import List

from .db import db, metadata, engine

# Import your models and schema
# from .model import PersonIn, Person
# from .schema import people

app = FastAPI()

@app.on_event("startup")
async def startup():
    metadata.create_all(engine)
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Write your endpoints here
@app.get("/")
def index():
    return {"message": "test"}
    
# Examples:
# @app.get("/people/", response_model=List[Person])
# async def read_people():
#     query = people.select()
#     return await db.fetch_all(query)

# @app.post("/people/", response_model=Person)
# async def create_person(person: PersonIn):
#     query = people.insert().values(name=person.name, age=person.age)
#     last_record_id = await db.execute(query)
#     return {**person.dict(), "id": last_record_id}
