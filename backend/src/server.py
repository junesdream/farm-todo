from contextlib import asynccontextmanager
import os
import sys
from datetime import datetime

from fastapi import FastAPI, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import uvicorn

# Custom DAL imports
from dal import ToDoDAL, ListSummary, ToDoList

# Configuration constants
COLLECTION_NAME = "todo_lists"
MONGODB_URI = os.environ["MONGODB_URI"]
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}

# Lifespan context manager to handle startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client.get_default_database()

    # Database connectivity check
    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")

    app.todo_dal = ToDoDAL(database.get_collection(COLLECTION_NAME))
    yield  # Yield control back to the FastAPI event loop
    client.close()  # Cleanup the client resources

app = FastAPI(lifespan=lifespan, debug=DEBUG)

# Endpoints for handling to-do lists
@app.get("/api/lists")
async def get_all_lists() -> list[ListSummary]:
    return [list_async for list_async in app.todo_dal.list_todo_lists()]

@app.post("/api/lists", status_code=status.HTTP_201_CREATED)
async def create_todo_list(new_list: NewList) -> NewListResponse:
    response_id = await app.todo_dal.create_todo_list(new_list.name)
    return NewListResponse(id=response_id, name=new_list.name)

@app.get("/api/lists/{list_id}")
async def get_list(list_id: str) -> ToDoList:
    return await app.todo_dal.get_todo_list(list_id)

@app.delete("/api/lists/{list_id}")
async def delete_list(list_id: str) -> bool:
    return await app.todo_dal.delete_todo_list(list_id)

# Models for new items in the list
class NewItem(BaseModel):
    label: str

class NewItemResponse(BaseModel):
    id: str
    label: str

@app.post("/api/lists/{list_id}/items/", status_code=status.HTTP_201_CREATED)
async def create_item(list_id: str, new_item: NewItem) -> ToDoList:
    return await app.todo_dal.create_item(list_id, new_item.label)

@app.delete("/api/lists/{list_id}/items/{item_id}")
async def delete_item(list_id: str, item_id: str) -> ToDoList:
    return await app.todo_dal.delete_item(list_id, item_id)

# Patch method for updating the checked state of an item
class ToDoItemUpdate(BaseModel):
    item_id: str
    checked_state: bool

@app.patch("/api/lists/{list_id}/checked_state")
async def set_checked_state(list_id: str, update: ToDoItemUpdate) -> ToDoList:
    return await app.todo_dal.set_checked_state(list_id, update.item_id, update.checked_state)

# Dummy API endpoint to return a timestamp and generated ObjectId
class DummyResponse(BaseModel):
    id: str
    when: datetime

@app.get("/api/dummy")
async def get_dummy() -> DummyResponse:
    return DummyResponse(id=str(ObjectId()), when=datetime.now())

# Main function to run the server
def main(argv=sys.argv[1:]):
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        print("Server stopped manually")

if __name__ == "__main__":
    main()
