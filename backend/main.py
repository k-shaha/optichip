from fastapi import FastAPI
from backend.simulator import simulate_workload 
from backend.logger import log_simulation, CSV_LOG
from backend.models import SimulationRequest, SimulationResponse
from datetime import datetime
import json
import os

app = FastAPI()

# ------------------------
# Run a simulation
# ------------------------
@app.post("/simulate", response_model=SimulationResponse)
def run_simulation(sim_req: SimulationRequest): 
    results = simulate_workload(
        sim_req.memory_blocks, 
        sim_req.delay, 
        sim_req.memory_type
    )

    timestamp = log_simulation(sim_req, results)

    return {
        "timestamp": timestamp,
        "config": sim_req, 
        "results": results 
    }

# ------------------------
# Get entire simulation log
# ------------------------
@app.get("/log")
def get_log():
    data = []
    try:
        with open("backend/runs_log_cleaned.csv", "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue  # skip blank lines
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue  # skip malformed
        return data
    except FileNotFoundError:
        return []
    except Exception as e:
        return {"error": str(e)}

# ------------------------
# Clear the log file
# ------------------------
@app.post("/reset")
def reset_log():
    try:
        with open("backend/runs_log_cleaned.csv", "w") as f:
            f.write("")  # clear file
        return {"status": "log reset"}
    except Exception as e:
        return {"error": str(e)}
