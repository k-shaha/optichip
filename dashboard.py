import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import json

st.set_page_config(page_title="OptiChip GPU Simulator", layout="wide")

# --------------------
# Green GPU Theme (#40ab34)
# --------------------
st.markdown("""
    <style>
        :root {
            --primary-color: #40ab34;
            --background-color: #0f0f0f;
        }

        body, .main {
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
# Title & Controls
# --------------------
st.title("OptiChip GPU Workload Simulator")
st.markdown("### Simulation Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    memory_blocks = st.slider("Memory Blocks", 1, 32, 8)

with col2:
    delay = st.radio("Delay", options=[True, False], format_func=lambda x: "Enabled" if x else "Disabled")

with col3:
    memory_type = st.selectbox("Memory Type", ["global", "shared"])

run_clicked = st.button("Run Simulation")

# --------------------
# Simulation API Call
# --------------------
sim_result = None
if run_clicked:
    try:
        payload = {
            "memory_blocks": memory_blocks,
            "delay": delay,
            "memory_type": memory_type
        }
        response = requests.post("http://localhost:8000/simulate", json=payload)
        response.raise_for_status()
        sim_result = response.json()
        st.success("Simulation complete.")
    except Exception as e:
        st.error(f"Simulation failed: {e}")

# --------------------
# Show Result of Most Recent Simulation
# --------------------
if sim_result:
    df = pd.DataFrame(sim_result["results"])
    df.columns = ["Block ID", "Transfer Time (s)"]

    st.markdown("### Transfer Time per Block")

    fig = go.Figure(data=[
        go.Bar(
            x=df["Block ID"],
            y=df["Transfer Time (s)"],
            marker_color='#40ab34'
        )
    ])
    fig.update_layout(
        plot_bgcolor="#0f0f0f",
        paper_bgcolor="#0f0f0f",
        font_color="#40ab34",
        xaxis_title="Block ID",
        yaxis_title="Transfer Time (s)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Raw Transfer Table")
    st.dataframe(df.style.set_properties(**{
        'background-color': '#0f0f0f',
        'color': '#40ab34',
        'border-color': '#40ab34',
        'text-align': 'center'
    }), use_container_width=True)
else:
    st.info("Run a simulation to view results.")

# --------------------
# Simulation History
# --------------------
st.markdown("---")
st.markdown("### Simulation History")

if st.button("Restart (Clear History)"):
    try:
        reset = requests.post("http://localhost:8000/reset")
        if reset.status_code == 200:
            st.success("Simulation log cleared.")
    except Exception as e:
        st.error(f"Failed to clear log: {e}")

try:
    log_response = requests.get("http://localhost:8000/log")
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

        history_df = pd.DataFrame(records)
        st.dataframe(history_df.style.set_properties(**{
            'background-color': '#0f0f0f',
            'color': '#40ab34',
            'text-align': 'center'
        }), use_container_width=True)
    else:
        st.info("No history found yet.")
except Exception as e:
    st.error(f"Failed to load history: {e}")
