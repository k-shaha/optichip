import streamlit as st
import requests

st.set_page_config(page_title="OptiChip Simulator", layout="centered")

st.markdown(
    "<h1 style='color:#2ECC71; font-size: 36px;'>OptiChip: GPU Workload Visualizer</h1>", 
    unsafe_allow_html=True
)

with st.form("sim-form"):
    st.subheader("Simulation Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        memory_blocks = st.slider("Memory Blocks", 1, 64, 8)
    with col2:
        delay = st.slider("Delay (ms)", 0, 500, 100)
    
    memory_type = st.selectbox("Memory Type", ["DRAM", "SRAM", "HBM"])
    
    submitted = st.form_submit_button("Run Simulation")

if submitted:
    payload = {
        "memory_blocks": memory_blocks,
        "delay": delay,
        "memory_type": memory_type
    }
    try:
        res = requests.post("http://127.0.0.1:8000/simulate", json=payload)
        if res.status_code == 200:
            data = res.json()
            st.success(f"Simulation completed at {data['timestamp']}")
            st.code("\n".join(data["results"]), language="text")
        else:
            st.error("Simulation failed. Please check your backend.")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

if st.button("View Previous Logs"):
    try:
        res = requests.get("http://127.0.0.1:8000/log")
        if res.status_code == 200 and res.json().get("log"):
            log = res.json()["log"]
            st.subheader("Simulation History")
            for row in log[1:]:  # skip header
                st.text(f"{row[0]} | {row[1]} | {row[2]} blocks | {row[3]} ms")
        else:
            st.info("No logs found.")
    except Exception as e:
        st.error(f"Error retrieving logs: {e}")
