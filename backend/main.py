from fastapi import FastAPI
from pydantic import BaseModel
from simulator import simulate_workload
from workload_logger import log_workload, read_log
from datetime import datetime

app = FastAPI()

class SimulationRequest(BaseModel):
    memory_blocks: int
    memory_type: str
    enable_delay: bool

@app.post("/simulate")
def simulate(request: SimulationRequest):
    print("🔥 /simulate called")

    results = simulate_workload(
        memory_blocks=request.memory_blocks,
        memory_type=request.memory_type,
        enable_delay=request.enable_delay
    )

    # ✅ Sanity check
    assert isinstance(results, list) and isinstance(results[0], dict)

    payload = {
        "timestamp": datetime.now().isoformat(),
        "memory_type": request.memory_type,
        "delay": request.enable_delay,
        "results": results
    }

    log_workload(payload)
    return payload

@app.get("/log")
def get_log():
    return read_log()
