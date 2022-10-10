import pymongo
import argparse
import os
import sys
import json
import time
from datetime import datetime

def main(args, db):
    collection = db[args.collection]
    collection.create_index("value", unique=True)
    collection.create_index("created_at", unique=False)
    collection.create_index("updated_at", unique=False)
    collection.create_index("status", unique=False)
    collection.create_index("source", unique=False)
    
    print(f"Processing file {args.collection}")
    with open(args.seed_path+args.collection, "r") as f:
        for line in f:
            try:
                print(line.strip())
                data = {
                    "value": line.strip(),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "status": "seed",
                    "disposition": ["seed"],
                }
                collection.update_one({"value": line.strip()}, {"$set": data, "$inc":{"count":1}}, upsert=True)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Line: {line}")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=27017)
    parser.add_argument("--db", type=str, default="psycho_dev")
    parser.add_argument("--collection", type=str, required=True)
    parser.add_argument("--seed_path", type=str, default="seeds/")
    args = parser.parse_args()
    client = pymongo.MongoClient(args.host, args.port)
    db = client[args.db]
    main(args, db)