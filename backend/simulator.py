import time 
import numpy as np 

# Simulates a workload
# Parameters:
# - memory_blocks: Number of memory blocks to simulate
# - delay: Delay in seconds between each block transfer

def simulate_workload(memory_blocks = 4, delay = 0.5): 
    results = []
    if delay: 
        for i in range(memory_blocks): 
            time.sleep(delay) # simulates delay for each block
            latency = np.random.uniform(0.3, 0.7) # fake, randomly generated latency value
            results.append({ # adds block and transfer time to results
                "block_id": i,
                "transfer_time": latency,
            })
        return results # returns results list 