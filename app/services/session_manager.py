# app/services/session_manager.py

import json
from pathlib import Path

SESSION_FILE = Path("last_collection.json")

def set_last_collection(collection_name: str):
    data = {"last_collection": collection_name, "all_collections": []}
    if SESSION_FILE.exists():
        data = json.loads(SESSION_FILE.read_text())

    data["last_collection"] = collection_name
    if collection_name not in data.get("all_collections", []):
        data["all_collections"].append(collection_name)

    SESSION_FILE.write_text(json.dumps(data))

def get_last_collection() -> str | None:
    if SESSION_FILE.exists():
        data = json.loads(SESSION_FILE.read_text())
        return data.get("last_collection")
    return None

def get_all_collections() -> list[str]:
    if SESSION_FILE.exists():
        data = json.loads(SESSION_FILE.read_text())
        return data.get("all_collections", [])
    return []
