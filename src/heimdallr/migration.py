"""
DB migration script
"""
import os

import pandas as pd
from pymongo import MongoClient

from heimdallr.domain.models.assignment import Assignment
from heimdallr.settings.mongo_settings import MongoSettings


def get_entries() -> pd.DataFrame:
    """
    Get the entries from the training.csv file.
    """
    upper_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    path = os.path.join(upper_dir, "db", "training.csv")
    print(f"Loading entries from {path}...")
    return pd.read_csv(path)


def to_list(row: str) -> list[str]:
    """
    Convert a row to a list.
    """
    try:
        return row.removeprefix("[").removesuffix("]").split(",")
    except ValueError:
        return []


if __name__ == "__main__":
    # Mongo DB Config
    print("DB Migration Script - WARNING: This script will drop the current Assignment Collection.")
    MONGO_URL = MongoSettings().CLIENT
    DB_NAME = MongoSettings().DATABASE
    COLLECTION_NAME = Assignment.__name__.lower()
    print(f"Connecting to MongoDB(uri={MONGO_URL}, db={DB_NAME}, collection={COLLECTION_NAME})")
    mongo_client: MongoClient = MongoClient(MONGO_URL, uuidRepresentation="standard")
    mongo_client.get_database(DB_NAME).drop_collection(COLLECTION_NAME)
    print("Connected successfully.")

    # prepare entries
    entries = get_entries().to_dict("records")
    print(f"Inserting {len(entries)} entries...")
    mapped_entries = []
    for entry in entries:
        entry["content"] = to_list(entry["content"])
        entry["similarities"] = []
        mapped_entries.append(entry)

    # insert
    result = mongo_client.get_database(DB_NAME).get_collection(COLLECTION_NAME).insert_many(mapped_entries)
    count = len(result.inserted_ids)
    print(f"Inserted {len(result.inserted_ids)} entries successfully.")

    # verify
    print("Verifying...")
    cursor = mongo_client.get_database(DB_NAME).get_collection(COLLECTION_NAME).find({})
    TOTAL_ASSIGNMENTS = 0
    for document in cursor:
        print(f"[{TOTAL_ASSIGNMENTS}/{count - 1}] {Assignment(**document)}")
        TOTAL_ASSIGNMENTS += 1
    print(f"Verified {TOTAL_ASSIGNMENTS} entries.")
    print("Done.")
