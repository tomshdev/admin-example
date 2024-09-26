from datetime import datetime
import logging
from typing import List
from uuid import uuid4
from mongoengine import get_db as mongoengine_get_db


logger = logging.getLogger(__name__)


class History:
    def __init__(self, session_id: str = None):
        self.session_id = session_id or  str(uuid4())
        db = mongoengine_get_db
        self.collection = db["history"]
        self.collection.create_index("SessionId")

    @property
    def messages(self) -> List[Any]:  # type: ignore
        """Retrieve the messages from MongoDB"""
        cursor = self.collection.find({"SessionId": self.session_id}).sort("_id")
        return list(cursor)

    def add_message(self, message) -> None:
        """Append the message to the record in MongoDB"""
        self.collection.insert_one(
            {
                "SessionId": self.session_id,
                "Message": message,
                "App": self._app_metadata()
            })

    def _app_metadata(self):
        return {
            "version": 1,
            "timestamp": str(datetime.now()),
        }

    # filter history messages for presenting in the chat/history/viewr 
    # based on filters function:
    def _build_query(self, start_date, end_date):

        # Prepare the query
        query = {}

        if start_date:
            query["App.timestamp"] = {"$gte": start_date}
        if end_date:
            if "App.timestamp" in query:
                query["App.timestamp"]["$lte"] = end_date
            else:
                query["App.timestamp"] = {"$lte": end_date}

        return query

    def get_filtered_documents(self, start_date, end_date):
        query = self._build_query(start_date, end_date)
        cursor = self.collection.find(query).sort("_id")
        return list(cursor)
