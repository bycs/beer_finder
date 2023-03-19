from datetime import datetime

from pymongo import MongoClient
from pymongo.database import Database
from telegram import Update

from config import MONGO_URI


client: MongoClient = MongoClient(MONGO_URI)

db = client.bot_db


def logging_commands(database: Database, update: Update, command: str) -> None:
    database.log_commands.insert_one(
        {
            "command": command,
            "user_id": update.effective_user.id,  # type: ignore
            "chat_id": update.message.chat.id,  # type: ignore
            "datetime": datetime.now(),
        }
    )
