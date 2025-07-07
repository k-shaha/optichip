from pydantic import BaseModel
from typing import Literal

class SimulationRequest(BaseModel):
    memory_blocks: int
    memory_type: Literal["global", "shared", "texture"]
    delay: bool

class SimulationResponse(BaseModel):
    timestamp: str
    config: SimulationRequest
    results: dict
