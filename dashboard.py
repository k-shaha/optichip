import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

st.set_page_config(page_title="OptiChip GPU Simulator", layout="wide")
API_BASE = "http://localhost:8000"

# --------------------
# Green GPU Theme (#40ab34)
# --------------------
st.markdown("""
    <style>
        :root {
            --primary-color: #40ab34;
            --background-color: #0f0f0f;
        }
        body, .main, .block-container {
            background-color: #0f0f0f;
            color: #40ab34;
        }
        .stButton > button {
            background-color: #40ab34 !important;
            color: #0f0f0f !important;
            border: none;
        }
        .stSlider > div {
            color: #40ab34 !important;
        }
        input[type=range]::-webkit-slider-thumb {
            background: #40ab34;
        }
        input[type=range]::-webkit-slider-runnable-track {
            background: #40ab34;
        }
        .stRadio > div, .stSelectbox > div {
            color: #40ab34 !important;
        }
        div[data-baseweb="radio"] label {
            color: #40ab34 !important;
        }
        .stDataFrame tbody td {
            text-align: center;
            color: #40ab34 !important;
            background-color: #0f0f0f !important;
        }
        .stDataFrame thead th {
            color: #40ab34 !important;
            background-color: #111 !important;
        }
        h1, h2, h3 {
            color: #40ab34;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------
# Title & Input
# --------------------
st.title("OptiChip - GPU Workload Visualizer")

col1, col2, col3 = st.columns(3)

with col1:
    memory_blocks = st.slider("Number of Memory Blocks", 1, 20, 8)

with col2:
    delay = st.checkbox("Enable Real-Time Delay")

with col3:
    memory_type = st.radio("Select Memory Type", ["global", "shared"])

# --------------------
# Run Button
# --------------------
if st.button("Run Simulation"):
    try:
        payload = {
            "memory_blocks": memory_blocks,
            "delay": delay,
            "memory_type": memory_type
        }
        response = requests.post(f"{API_BASE}/simulate", json=payload)
        response.raise_for_status()
        st.success(f"Simulation complete at {response.json()['timestamp']}")
    except Exception as e:
        st.error(f"Simulation failed: {e}")

# --------------------
# Pull + Show Full History
# --------------------
st.markdown("### Simulation History")

try:
    log_response = requests.get(f"{API_BASE}/log")
    log_response.raise_for_status()
    all_runs = log_response.json()

    if all_runs:
        records = []
        for entry in all_runs:
            results = entry["results"]
            if isinstance(results, str):
                results = json.loads(results.replace("'", "\""))
            for block in results:
                records.append({
                    "Timestamp": entry.get("timestamp"),
                    "Memory Type": entry.get("memory_type", "n/a"),
                    "Delay": entry.get("delay", False),
                    "Block ID": block["block_id"],
                    "Transfer Time (s)": block["transfer_time"]
                })

        df = pd.DataFrame(records)

        # Bar chart
        fig = px.bar(
            df,
            x="Block ID",
            y="Transfer Time (s)",
            color_discrete_sequence=["#40ab34"],
            title="Transfer Time by Block",
            labels={"Block ID": "Block ID", "Transfer Time (s)": "Transfer Time (s)"}
        )
        fig.update_layout(
            plot_bgcolor="#0f0f0f",
            paper_bgcolor="#0f0f0f",
            font_color="#40ab34"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --------------------
        # Restart Button (below chart)
        # --------------------
        if st.button("Restart (Clear History)"):
            try:
                requests.post(f"{API_BASE}/reset")
                st.success("Simulation log cleared.")
            except Exception as e:
                st.error(f"Failed to reset log: {e}")

        # Raw table
        st.markdown("### Raw Transfer Data")
        st.dataframe(df.style.set_properties(**{
            'background-color': '#0f0f0f',
            'color': '#40ab34',
            'text-align': 'center'
        }), use_container_width=True)
    else:
        st.info("No history found yet.")
except Exception as e:
    st.error(f"Failed to load history: {e}")
