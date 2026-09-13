import json


def read_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def clear_json_file(file_path: str):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump({}, file)
