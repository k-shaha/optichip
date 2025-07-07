import csv
import json
import os
from datetime import datetime

CLEAN_CSV = "runs_log_clean.csv"
RAW_JSONL = "runs_log.jsonl"


def save_log(entry):
    # Save raw JSONL
    with open(RAW_JSONL, "a") as raw_file:
        raw_file.write(json.dumps(entry) + "\n")

    # Save cleaned CSV with headers
    save_log_to_csv(entry)


def save_log_to_csv(entry, filename=CLEAN_CSV):
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "memory_type", "delay", "block_id", "transfer_time"])

        if not file_exists:
            writer.writeheader()

        results = entry["results"]
        if isinstance(results, str):
            results = json.loads(results.replace("'", "\""))

        for block in results:
            writer.writerow({
                "timestamp": entry.get("timestamp"),
                "memory_type": entry.get("memory_type", "n/a"),
                "delay": entry.get("delay", False),
                "block_id": block["block_id"],
                "transfer_time": block["transfer_time"]
            })


def load_clean_csv(filename=CLEAN_CSV):
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def clear_logs():
    for f in [CLEAN_CSV, RAW_JSONL]:
        if os.path.exists(f):
            os.remove(f)
