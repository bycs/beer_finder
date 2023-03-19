from datetime import datetime

from pymongo import MongoClient

from config import MONGO_URI


client: MongoClient = MongoClient(MONGO_URI)

db = client.bot_db


def logging_commands(db, user_id: int, chat_id: int, command: str) -> None:
    db.log_commands.insert_one(
        {
            "command": command,
            "user_id": user_id,
            "chat_id": chat_id,
            "datetime": datetime.now(),
        }
    )
