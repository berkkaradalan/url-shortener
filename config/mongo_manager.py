import sys
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config.env import settings


class MongoManager:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        max_retries = settings.MONGODB_MAX_RETRIES
        retry_delay = settings.MONGODB_RETRY_DELAY

        for attempt in range(1, max_retries + 1):
            try:
                print(f"Attempting to connect to MongoDB (attempt {attempt}/{max_retries})...")

                if settings.MONGODB_USERNAME and settings.MONGODB_PASSWORD:
                    connection_string = (
                        f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@"
                        f"{settings.MONGODB_URL.replace('mongodb://', '')}"
                    )
                else:
                    connection_string = settings.MONGODB_URL

                self.client = MongoClient(
                    connection_string,
                    serverSelectionTimeoutMS=5000
                )

                self.client.admin.command('ping')

                self.db = self.client[settings.MONGODB_DATABASE]

                print(f"Successfully connected to MongoDB database: {settings.MONGODB_DATABASE}")
                return True

            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                print(f"Failed to connect to MongoDB: {str(e)}")

                if attempt < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Failed to connect to MongoDB after {max_retries} attempts.")
                    print("Exiting application...")
                    sys.exit(1)

            except Exception as e:
                print(f"Unexpected error while connecting to MongoDB: {str(e)}")
                print("Exiting application...")
                sys.exit(1)

        return False

    def get_database(self):
        if self.db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.db

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

mongo_manager = MongoManager()
