from pydantic import BaseModel 
from typing import List, Literal 
from datetime import datetime

class SimulationRequest(BaseModel):
   memory_blocks : int 
   delay: bool
   memory_type: Literal["global", "shared"]

class BlockResult(BaseModel):
    block_id: int
    transfer_time: float

class SimulationResponse(BaseModel):
    timestamp: datetime
    config: SimulationRequest
    results: List [BlockResult]


