# LLM-IoT Agricultural Assistant (Streamlit Prototype)
# Covers 10 executable use cases with synthetic data, LLM (OpenAI), agentic actions, and feedback loop

import streamlit as st
import pandas as pd
import random
import openai
import json

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# ---- Inputs and Synthetic Data Generation ----

def generate_synthetic_inputs(use_case):
    if use_case == "Precision Irrigation Control":
        return {
            "soil_moisture": random.uniform(10, 35),
            "rain_forecast": random.choice(["None", "Light", "Moderate", "Heavy"]),
            "evapotranspiration": round(random.uniform(3, 8), 2)
        }
    elif use_case == "Autonomous Fertilizer Application":
        return {
            "soil_n": random.choice(["Low", "Medium", "High"]),
            "soil_p": random.choice(["Low", "Medium", "High"]),
            "soil_k": random.choice(["Low", "Medium", "High"]),
            "crop_stage": random.choice(["Vegetative", "Flowering", "Maturity"])
        }
    elif use_case == "Pest & Disease Intervention":
        return {
            "crop_image_desc": "Yellowing leaves, spots observed.",
            "humidity": random.randint(50, 90),
            "temperature": random.randint(20, 35)
        }
    elif use_case == "Crop Growth Stage Monitoring & Action":
        return {
            "ndvi_value": random.uniform(0.3, 0.9),
            "current_stage": random.choice(["Tillering", "Booting", "Flowering"])
        }
    elif use_case == "Soil Health Remediation Actions":
        return {
            "soil_ph": round(random.uniform(4.5, 8.0), 2),
            "salinity": round(random.uniform(0.2, 2.5), 2)
        }
    elif use_case == "Weather-Responsive Farm Planning":
        return {
            "next_3_days_rain_mm": [random.randint(0, 20) for _ in range(3)],
            "temperature_forecast": [random.randint(20, 40) for _ in range(3)]
        }
    elif use_case == "Harvest Timing & Post-Harvest Handling":
        return {
            "ripeness_index": round(random.uniform(0.6, 1.0), 2),
            "storage_temperature": random.randint(4, 25)
        }
    elif use_case == "Labor & Machinery Task Assignment":
        return {
            "field_workload": random.choice(["High", "Medium", "Low"]),
            "available_labor": random.randint(1, 10),
            "equipment_status": random.choice(["All Available", "Tractor Fault", "Low Fuel"])
        }
    elif use_case == "Environmental Compliance Monitoring":
        return {
            "nitrate_level": round(random.uniform(10, 50), 2),
            "water_ph": round(random.uniform(6.0, 8.5), 2)
        }
    elif use_case == "Input Cost Optimization":
        return {
            "fertilizer_price_n": random.randint(4000, 8000),
            "last_year_avg_price_n": random.randint(5000, 7000),
            "market_trend": random.choice(["Rising", "Stable", "Falling"])
        }

# ---- LLM Decision Engine ----

def llm_decision_engine(use_case, input_data):
    prompt = f"""
You are a smart agricultural assistant helping farmers automate decisions.
Use case: {use_case}
Inputs: {json.dumps(input_data, indent=2)}
Generate:
1. Summary of decision
2. Action to take
3. Command to send to IoT system (standardized)
4. Reasoning for the action
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert agronomic agent."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

# ---- Streamlit Interface ----
st.title("🌾 LLM-IoT Agricultural Assistant")

use_cases = [
    "Precision Irrigation Control",
    "Autonomous Fertilizer Application",
    "Pest & Disease Intervention",
    "Crop Growth Stage Monitoring & Action",
    "Soil Health Remediation Actions",
    "Weather-Responsive Farm Planning",
    "Harvest Timing & Post-Harvest Handling",
    "Labor & Machinery Task Assignment",
    "Environmental Compliance Monitoring",
    "Input Cost Optimization"
]

selected_use_case = st.selectbox("Select a Use Case", use_cases)

if st.button("Generate Synthetic Input and Run Engine"):
    inputs = generate_synthetic_inputs(selected_use_case)
    st.subheader("🔍 Synthetic Input Data")
    st.json(inputs)

    with st.spinner("Thinking..."):
        decision = llm_decision_engine(selected_use_case, inputs)

    st.subheader("🤖 LLM Decision Output")
    st.text(decision)

    st.subheader("📡 IoT Command (Simulated Execution)")
    st.code("Sending command to field controller... ✅")

    st.subheader("🔁 Feedback Loop")
    st.text("Device confirmed action. Logs stored for traceability.")

    st.success("Use case completed!")

st.markdown("""
---
**How it works:**
- Each use case has predefined inputs.
- Synthetic data mimics real sensor values.
- OpenAI LLM reasons and generates agronomic decisions.
- Actions are simulated and logged in a standard format.
""")
