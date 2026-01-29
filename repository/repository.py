from config.mongo_manager import mongo_manager
from models.models import URLMapping

class URLRepository:
    def __init__(self):
        self.collection_name = "url_mappings"

    def get_collection(self):
        db = mongo_manager.get_database()
        return db[self.collection_name]

    def insert(self, url_mapping: URLMapping) -> bool:
        try:
            collection = self.get_collection()
            document = {
                "url_id": url_mapping.url_id,
                "long_url": url_mapping.long_url,
                "created_at": url_mapping.created_at
            }
            collection.insert_one(document)
            return True
        except Exception as e:
            print(f"Error inserting URL mapping: {str(e)}")
            return False

    def get_by_url_id(self, url_id: str) -> URLMapping | None:
        try:
            collection = self.get_collection()
            document = collection.find_one({"url_id": url_id})

            if document:
                return URLMapping(
                    url_id=document["url_id"],
                    long_url=document["long_url"],
                    created_at=document["created_at"]
                )
            return None
        except Exception as e:
            print(f"Error getting URL mapping: {str(e)}")
            return None

    def get_by_long_url(self, long_url: str) -> URLMapping | None:
        try:
            collection = self.get_collection()
            document = collection.find_one({"long_url": long_url})

            if document:
                return URLMapping(
                    url_id=document["url_id"],
                    long_url=document["long_url"],
                    created_at=document["created_at"]
                )
            return None
        except Exception as e:
            print(f"Error getting URL mapping by long URL: {str(e)}")
            return None

    def exists(self, url_id: str) -> str | None:
        mapping = self.get_by_url_id(url_id)
        return mapping.long_url if mapping else None

url_repository = URLRepository()