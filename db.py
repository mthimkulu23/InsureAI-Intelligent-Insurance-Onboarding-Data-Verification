import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger("insureai.db")

class MemoryCollection:
    """Fallback in-memory collection simulating basic PyMongo operations."""
    def __init__(self, name):
        self.name = name
        self._data = {}

    def insert_one(self, doc):
        doc_id = str(doc.get('_id', len(self._data) + 1))
        doc['_id'] = doc_id
        self._data[doc_id] = dict(doc)
        class InsertResult:
            def __init__(self, id_val):
                self.inserted_id = id_val
        return InsertResult(doc_id)

    def find(self, filter_dict=None):
        filter_dict = filter_dict or {}
        results = []
        for item in self._data.values():
            match = True
            for k, v in filter_dict.items():
                if item.get(k) != v:
                    match = False
                    break
            if match:
                results.append(dict(item))
        return results

    def find_one(self, filter_dict):
        results = self.find(filter_dict)
        return results[0] if results else None

    def update_one(self, filter_dict, update_dict):
        item = self.find_one(filter_dict)
        if item:
            target_id = item['_id']
            if '$set' in update_dict:
                for k, v in update_dict['$set'].items():
                    self._data[target_id][k] = v
            class UpdateResult:
                matched_count = 1
                modified_count = 1
            return UpdateResult()
        class UpdateResult:
            matched_count = 0
            modified_count = 0
        return UpdateResult()

    def delete_many(self, filter_dict=None):
        filter_dict = filter_dict or {}
        if not filter_dict:
            # Empty filter means delete all
            self._data.clear()
            return
        to_del = [k for k, v in self._data.items()
                  if all(v.get(fk) == fv for fk, fv in filter_dict.items())]
        for k in to_del:
            del self._data[k]

    def count_documents(self, filter_dict=None):
        return len(self.find(filter_dict))


class MemoryDatabase:
    """Fallback database wrapper."""
    def __init__(self):
        self.documents = MemoryCollection("documents")
        self.onboardings = MemoryCollection("onboardings")
        self.anomalies = MemoryCollection("anomalies")
        self.audit_logs = MemoryCollection("audit_logs")
        self.magic_links = MemoryCollection("magic_links")
        self.is_fallback = True

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(name)
        coll = MemoryCollection(name)
        setattr(self, name, coll)
        return coll

    def __getitem__(self, item):
        return getattr(self, item)


_db_instance = None
_mongo_client = None  # Kept for clean shutdown


def reset_db():
    """Reset the cached DB instance (useful in tests or to force reconnect)."""
    global _db_instance, _mongo_client
    if _mongo_client is not None:
        try:
            _mongo_client.close()
        except Exception:
            pass
        _mongo_client = None
    _db_instance = None


def get_db(app=None):
    global _db_instance, _mongo_client
    if _db_instance is not None:
        return _db_instance

    mongodb_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/insureai')
    db_name = os.environ.get('DB_NAME', 'insureai_db')

    # Try connecting to MongoDB Atlas or local MongoDB
    if mongodb_uri and "mongodb" in mongodb_uri.lower():
        try:
            client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=1000)
            client.admin.command('ping')
            db = client[db_name]
            db.is_fallback = False
            logger.info("Successfully connected to MongoDB Atlas / Server.")
            _mongo_client = client
            _db_instance = db
            return db
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.warning(f"MongoDB connection fallback: {e}")
            # Close the failed client to avoid resource leak
            try:
                MongoClient(mongodb_uri, serverSelectionTimeoutMS=1000).close()
            except Exception:
                pass

    _db_instance = MemoryDatabase()
    return _db_instance
