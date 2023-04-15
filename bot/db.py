from datetime import datetime

from pymongo import MongoClient
from pymongo.database import Database
from telegram import Update

from config import MONGO_URI


client: MongoClient = MongoClient(MONGO_URI)

db: Database = client.get_database("bot_db")


def logging_commands(database: Database, update: Update, command: str) -> None:
    assert update.effective_user is not None, "update.effective_user must not be None"
    assert update.message is not None, "update.message must not be None"

    database.get_collection("log_commands").insert_one(
        {
            "command": command,
            "user_id": update.effective_user.id,
            "chat_id": update.message.chat.id,
            "datetime": datetime.now(),
        }
    )


def logging_search_query(
    database: Database, update: Update, search_query: dict, command: str
) -> None:
    assert update.effective_user is not None, "update.effective_user must not be None"

    database.get_collection("log_search_query").insert_one(
        {
            "command": command,
            "user_id": update.effective_user.id,
            "search_query": search_query,
            "datetime": datetime.now(),
        }
    )


def get_number_use_command(database: Database) -> dict[str, str | int] | None:
    result = database.get_collection("log_commands").aggregate(
        [
            {"$group": {"_id": "$command", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$group": {"_id": None, "counts": {"$push": {"k": "$_id", "v": "$count"}}}},
            {"$replaceRoot": {"newRoot": {"$arrayToObject": "$counts"}}},
        ]
    )
    commands = next(result, None)
    return commands


def get_number_unique_users(database: Database) -> int:
    result: list[int] = database.get_collection("log_commands").distinct("user_id")
    return len(result)
