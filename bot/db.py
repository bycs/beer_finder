from datetime import datetime

from pymongo import MongoClient
from pymongo.database import Database
from telegram import Update

from config import MONGO_URI


client: MongoClient = MongoClient(MONGO_URI)

db = client.bot_db


def logging_commands(database: Database, update: Update, command: str) -> None:
    assert update.effective_user is not None, "update.effective_user must not be None"
    assert update.message is not None, "update.message must not be None"

    database.log_commands.insert_one(
        {
            "command": command,
            "user_id": update.effective_user.id,
            "chat_id": update.message.chat.id,
            "datetime": datetime.now(),
        }
    )
