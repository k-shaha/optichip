# OptiChip: GPU Workload Visualizer and Optimizer

OptiChip is a lightweight simulation platform designed to model GPU memory workloads under configurable conditions. Built to reflect real-world performance behaviors, OptiChip enables developers and researchers to analyze the impact of memory block size, delay intervals, and memory type selection on simulated GPU performance. It offers clean API access, robust data logging, and integration hooks for visualization and downstream analytics.

## Features

• Simulates GPU memory transfers with adjustable delay, block count, and memory type  
• Logs each simulation run to CSV with configuration metadata and timestamps  
• RESTful API built with FastAPI to support frontend and CLI-based interactions  
• Designed for integration with tools like Grafana or Streamlit for visual inspection  
• Modular architecture with extensibility for containerization and future GPU acceleration  

## Why This Project Matters

Modern AI applications are increasingly bottlenecked not by raw computation, but by memory access, bandwidth, and transfer latency. OptiChip was built to demystify these performance factors by giving users a way to simulate and measure memory transfer behavior in a controlled environment. It provides a foundation for deeper architectural experimentation and real-time observability tooling.

## Tech Stack and Tools

**Languages**  
• Python — Core simulation engine, logging logic, and backend API  
• Bash/PowerShell — Optional command-line tooling for running and analyzing simulations  

**Frameworks and Libraries**  
• FastAPI — High-performance backend API with clean documentation support  
• NumPy — Used to simulate realistic latency values based on probabilistic distributions  
• Pandas — For structured log parsing, data export, and historical data review
• datetime (Python stdlib) — For timestamps and structured logging 
• csv (Python stdlib) — For low-level CSV writing (used in log_simulation)

**Infrastructure Tools**  
• Git — Version control and collaboration  
• Docker (planned) — Containerization for consistent runtime environments  
• Grafana (optional) — Real-time dashboard for analyzing simulation results at scale  

**Interface and Visualization**  
• Streamlit — Interactive frontend for configuring simulations and viewing results in real-time 

## Project Structure
```
optichip/
├── backend/
│   ├── simulator.py         # Core simulation logic
│   ├── log_utils.py         # Handles structured CSV logging
│   └── main.py              # FastAPI app entrypoint
├── flatten_logs.py          # Merges and processes simulation logs
├── runs_log.csv             # Raw simulation history
├── processed_runs.csv       # Cleaned version of log data
├── frontend/
│   └── app.py               # Streamlit UI for simulation input
└── README.md
```

## Example Use Case

A user configures a simulation with 8 memory blocks, a 0.3-second delay per transfer, and HBM2 memory type. The API triggers the simulation and logs transfer latency per block. The results are stored in `runs_log.csv`, and can be visualized with a tool like Grafana or programmatically analyzed with Pandas.

## Future Improvements

• Containerize the application with Docker  
• Extend the simulation to model bandwidth saturation and concurrency effects  
• Build a richer frontend interface with configuration presets and charts  
• Add profiling modes for comparing memory types under identical load conditions  
• Integrate authentication for multi-user environments  

## Author

Developed by Khushi Shaha (khushishaha08@gmail.com)
