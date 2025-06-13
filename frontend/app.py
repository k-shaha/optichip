import streamlit as st 
import requests 
import pandas as pd
import time 

st.title("OptiChip - GPU Workload Visualizer")

# ----- UI Controls -----
memory_blocks = st.slider("Number of Memory Blocks", min_value=1, max_value=20, value=6, key="memory_blocks_slider")
delay = st.checkbox("Enable Real-Time Delay", value=True, key="delay_checkbox")
memory_type = st.radio("Select Memory Type", options=["global", "shared"], index=0, key="memory_type_radio")
run_button = st.button("Run Simulation", key="run_button")


# ----- Backend URL -----
API_URL = "http://127.0.0.1:8000/simulate"

#-----Trigger Simulation-----
if run_button: 
    with st.spinner("Simulating GPU transfer..."): 
        payload = {
            "memory_blocks": memory_blocks, 
            "delay": delay,
            "memory_type": memory_type
        }

        try: 
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            results = data["results"]
            from pandas import DataFrame as TrueDataFrame
            df = TrueDataFrame(results)
            
            st.text(f"✅ df is of type: {type(df)}")
            st.write("DataFrame preview:")
            st.write(df)
            if "transfer_time" in df.columns:
                st.bar_chart(df["transfer_time"])
                st.success(f"Simulation complete at {data['timestamp']}")
            else:
                st.error("⚠️ 'transfer_time' column missing from simulation result.")
            

            

            
            

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")   
