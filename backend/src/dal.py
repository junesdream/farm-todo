from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument
from pydantic import BaseModel
from uuid import uuid4

# Define data models for the to-do application
class ListSummary(BaseModel):
    id: str
    name: str
    item_count: int

    # Create from MongoDB document
    @staticmethod
    def from_doc(doc) -> "ListSummary":
        return ListSummary(
            id=str(doc["_id"]),
            name=doc["name"],
            item_count=doc["item_count"],
        )

class ToDoListItem(BaseModel):
    id: str
    label: str
    checked: bool

    # Convert MongoDB item document to data model
    @staticmethod
    def from_doc(item) -> "ToDoListItem":
        return ToDoListItem(
            id=item["_id"],
            label=item["label"],
            checked=item["checked"],
        )
    
class ToDoList(BaseModel):
    id: str
    name: str
    items: list[ToDoListItem]

    # Map document to ToDoList model
    @staticmethod
    def from_doc(doc) -> "ToDoList":
        return ToDoList(
            id=str(doc["_id"]),
            name=doc["name"],
            items=[ToDoListItem.from_doc(item) for item in doc["items"]],
        )

# Data access layer for handling to-do list operations
class ToDoDAL:
    def __init__(self, todo_collection: AsyncIOMotorCollection):
        self._todo_collection = todo_collection

    async def list_todo_lists(self):
        cursor = self._todo_collection.find(
            {},
            projection={"name": 1, "item_count": {"$size": "$items"}},
            sort=[("name", 1)]
        )
        async for doc in cursor:
            yield ListSummary.from_doc(doc)

    async def create_todo_list(self, name: str) -> str:
        response = await self._todo_collection.insert_one({"name": name, "items": []})
        return str(response.inserted_id)

    async def get_todo_list(self, list_id: str) -> ToDoList:
        doc = await self._todo_collection.find_one({"_id": ObjectId(list_id)})
        return ToDoList.from_doc(doc)

    async def delete_todo_list(self, list_id: str) -> bool:
        response = await self._todo_collection.delete_one({"_id": ObjectId(list_id)})
        return response.deleted_count == 1

    async def create_item(self, list_id: str, label: str) -> ToDoList:
        result = await self._todo_collection.update_one(
            {"_id": ObjectId(list_id)},
            {"$push": {"items": {"_id": uuid4(), "label": label, "checked": False}}},
            return_document=ReturnDocument.AFTER
        )
        return ToDoList.from_doc(result)

    async def update_item_checked_state(self, list_id: str, item_id: str, checked: bool) -> ToDoList:
        result = await self._todo_collection.update_one(
            {"_id": ObjectId(list_id), "items._id": item_id},
            {"$set": {"items.$.checked": checked}},
            return_document=ReturnDocument.AFTER
        )
        return ToDoList.from_doc(result)

    async def delete_item(self, list_id: str, item_id: str) -> ToDoList:
        result = await self._todo_collection.update_one(
            {"_id": ObjectId(list_id)},
            {"$pull": {"items": {"_id": item_id}}},
            return_document=ReturnDocument.AFTER
        )
        return ToDoList.from_doc(result)
