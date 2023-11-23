"""
GoogleFirestore
"""
from firebase_admin import firestore_async
from google.cloud.firestore_v1 import DocumentSnapshot
from google.cloud.firestore_v1.types import write

from app.clients.firebase.base import firebase_app
from app.config import settings


class GoogleFirestoreClient:
    """GoogleFirestoreClient"""

    def __init__(self):
        self.db = firestore_async.client(app=firebase_app)

    @staticmethod
    def gen_collection(collection: str):
        """

        :param collection:
        :return:
        """
        if collection.startswith(f"{settings.TELEGRAM_BOT_USERNAME}:"):
            return collection
        return f"{settings.TELEGRAM_BOT_USERNAME}:{collection}"

    async def set_document(self, collection: str, document: str, data: dict, **kwargs) -> write.WriteResult:
        """

        :param collection:
        :param document:
        :param data:
        :param kwargs:
        :return:
        """
        collection = self.gen_collection(collection)
        doc_ref = self.db.collection(collection).document(document)
        return await doc_ref.set(data, **kwargs)

    async def get_document(self, collection: str, document: str, **kwargs) -> DocumentSnapshot:
        """

        :param collection:
        :param document:
        :param kwargs:
        :return:
        """
        collection = self.gen_collection(collection)
        doc_ref = self.db.collection(collection).document(document)
        return await doc_ref.get(**kwargs)
