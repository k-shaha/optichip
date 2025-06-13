import time 
import numpy as np 

# Simulates a workload
# Parameters:
# - memory_blocks: Number of memory blocks to simulate
# - delay: Delay in seconds between each block transfer

def simulate_workload(memory_blocks : int, delay : bool, memory_type : str): 
    results = [] 
    for i in range(memory_blocks): 
        if delay > 0:
                time.sleep(delay) # simulates delay for each block
        
        # fake, randomly generated latency value
        if memory_type == "shared": 
             latency = np.random.uniform(0.05, 0.2) # less time --> less latency
        else: 
            latency = np.random.uniform(0.3, 0.7) # more time --> more latency
        
        results.append({ # adds block and transfer time to results
            "block_id": i,
            "transfer_time": latency,
        })
    return results # returns results list 