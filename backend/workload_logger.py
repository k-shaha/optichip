import csv
import os
import json

LOG_FILE = "runs_log.csv"

def log_workload(entry):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "memory_type", "delay", "results"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": entry["timestamp"],
            "memory_type": entry["memory_type"],
            "delay": str(entry["delay"]),  # ✅ store as string
            "results": json.dumps(entry["results"])  # ✅ store safely as JSON
        })

def read_log():
    history = []
    if not os.path.exists(LOG_FILE):
        return history

    with open(LOG_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["results"] = json.loads(row["results"])  # ✅ parse JSON
            except:
                row["results"] = []
            row["delay"] = row["delay"].lower() == "true"
            history.append(row)
    return history
