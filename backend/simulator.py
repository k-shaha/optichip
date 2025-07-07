import time
import numpy as np

def simulate_workload(memory_blocks: int, memory_type: str, enable_delay: bool):
    results = []
    for i in range(memory_blocks):
        if enable_delay:
            time.sleep(0.1)
        if memory_type == "shared":
            latency = np.random.uniform(0.05, 0.2)
        else:
            latency = np.random.uniform(0.3, 0.7)
        results.append({
            "block_id": i,
            "transfer_time": latency,
        })
    return results
