import os
import json
from datetime import datetime
from backend.models import SimulationRequest

# ✅ Corrected log path
CSV_LOG = "backend/runs_log_cleaned.csv"

def log_simulation(config: SimulationRequest, results):
    timestamp = datetime.utcnow().isoformat()

    row = {
        "timestamp": timestamp,
        "memory_blocks": config.memory_blocks,
        "delay": config.delay,
        "memory_type": config.memory_type,
        "results": results
    }

    # ✅ Append each run as a JSON string (one per line)
    with open(CSV_LOG, "a") as f:
        f.write(json.dumps(row) + "\n")

    return timestamp
