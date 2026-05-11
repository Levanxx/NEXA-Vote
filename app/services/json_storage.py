import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_json(filename):
    path = DATA_DIR / filename

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(filename, data):
    path = DATA_DIR / filename

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)