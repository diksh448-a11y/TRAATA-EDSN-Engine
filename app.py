import streamlit as st
import json
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="TRAATA | E-DSN Node Simulation",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ TRAATA - Distributed Environmental Disease Surveillance Node (E-DSN)")
st.markdown("**Split-Architecture Edge Diagnostic Engine & Prophylactic Intervention Pipeline**")

# --- SIDEBAR: SPLIT-ARCHITECTURE INPUTS ---
st.sidebar.header("📡 1. External Controller (Safe Zone)")
node_id = st.sidebar.text_input("E-DSN Node ID / Location", "Node #1042 - Residential Tank Sector A4")
battery_level = st.sidebar.slider("Li-Ion Battery Charge (%)", 0, 100, 88)
wifi_status = st.sidebar.selectbox("Network Transmission Link", ["Wi-Fi / MQTT Active", "Cellular Backup", "Offline Buffer"])

st.sidebar.header("🌊 2. Submerged Diagnostic Pod (IP68 Active Zone)")
water_temp = st.sidebar.slider("Water Temperature (°C)", 10.0, 45.0, 28.5)
hydrostatic_level = st.sidebar.slider("Hydrostatic Pressure (Water Level %)", 0, 100, 75)
absorbance_au = st.sidebar.slider("Optical Absorbance (A = ε·c·l AU)", 0.0, 3.0, 0.35)

pathogen_signature = st.sidebar.selectbox(
    "Optical Pathogen Signature (UV/Vis/NIR Spectrum)",
    [
        "Clean Baseline (Normal Spectrum)",
        "Coliform / Biological Protein Signature",
        "Chemical / Heavy Metal Drift (Arsenic/Nitrate)",
        "Thermal Biofilm / Algal Acceleration"
    ]
)

st.sidebar.header("⚡ 3. Autonomous Defense & API Controls")
uvc_shield = st.sidebar.checkbox("Activate 265nm UV-C Anti-Biofouling Shield", value=True)
api_key = st.sidebar.text_input("Groq / OpenAI API Key", type="password")

# --- MAIN DASHBOARD DISPLAY ---
st.subheader("1. Real-Time Telemetry Payload (Split-Architecture Node)")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Node Battery", f"{battery_level}%")
col2.metric("Water Temp", f"{water_temp} °C")
col3.metric("Hydrostatic Level", f"{hydrostatic_level}%")
col4.metric("Optical Absorbance", f"{absorbance_au} AU")

telemetry_payload = {
    "node_id": node_id,
    "battery_charge_pct": battery_level,
    "network_link": wifi_status,
    "water_temperature_c": water_temp,
    "hydrostatic_level_pct": hydrostatic_level,
    "optical_absorbance_au": absorbance_au,
    "detected_pathogen_signature": pathogen_signature,
    "uvc_anti_biofouling_active": uvc_shield
}

with st.expander("View Full JSON Telemetry Dispatch"):
    st.json(telemetry_payload)

st.subheader("2. Diagnostic Engine & Closed-Loop Remediation")

if st.button("Run E-DSN Diagnostic & Remediation Cycle"):
    # Rule check based on pitch deck specifications
    is_pathogen_flagged = pathogen_signature != "Clean Baseline (Normal Spectrum)"
    is_absorbance_high = absorbance_au >= 1.0
    is_critical_event = is_pathogen_flagged or is_absorbance_high
    
    if not api_key:
        st.info("No API Key detected. Executing local deterministic rule engine matching TRAATA deck specs:")
        
        if not is_critical_event:
            st.success("✅ DIAGNOSTIC STATUS: SAFE — Water quality strictly within safe BIS limits.")
            
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Threat Level", "LOW")
            res_col2.metric("Micro-Dosing Valve", "Closed (0.0 mL)")
            res_col3.metric("Consumption Safety Lockout", "Disengaged (Active)")
            
            st.markdown(f"""
            **System Diagnostics Breakdown:**
            * **Optical Fingerprinting:** Multi-wavelength absorbance is nominal (`{absorbance_au}` AU). No biological protein signatures detected.
            * **Anti-Biofouling Shield:** 265nm UV-C LED pulses active. DNA of settled micro-organisms continuously scrambled.
            * **Stagnation Predictor:** Low thermal risk at `{water_temp}`°C.
            * **Epidemiological Network:** Node status healthy. Routine telemetry heartbeat dispatched.
            """)
            
        else:
            st.error("⚠️ DIAGNOSTIC STATUS: CRITICAL — Last-Mile Contamination Intercepted at Source!")
            
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Threat Level", "CRITICAL")
            res_col2.metric("Micro-Dosing Valve", "Engaged (Micro-Dose Active)")
            res_col3.metric("Consumption Safety Lockout", "ENGAGED (Isolated)")
            
            st.markdown(f"""
            **System Diagnostics Breakdown:**
            * **Optical Fingerprinting:** Threat Flagged (`{pathogen_signature}`). Optical Absorbance drift detected (`{absorbance_au}` AU).
            * **Closed-Loop Intervention:** Micro-solenoid valve engaged. Releasing automated micro-dose of liquid sanitizer into domestic tank.
            * **Fail-Safe Protocol:** **Worst-Case Safety Lockout Loop Engaged.** Solenoid valve isolated the consumption supply line to prevent human ingestion.
            * **Epidemiological Radar:** Anomaly payload flagged with location coordinates and broadcast via MQTT to central public health dashboard.
            """)
            
    else:
        try:
            is_groq = api_key.startswith("gsk_")
            base_url = "https://api.groq.com/openai/v1" if is_groq else "https://api.openai.com/v1"
            model_name = "llama-3.3-70b-versatile" if is_groq else "gpt-4o-mini"
            
            client = OpenAI(base_url=base_url, api_key=api_key)
            
            system_prompt = """
            You are the TRAATA E-DSN Diagnostic Engine (Distributed Environmental Disease Surveillance Node).
            Evaluate the water telemetry according to these strict rules:
            1. If detected_pathogen_signature is 'Clean Baseline (Normal Spectrum)' AND optical_absorbance_au < 1.0, Threat Level is 'LOW'.
            2. If detected_pathogen_signature is NOT 'Clean Baseline (Normal Spectrum)' OR optical_absorbance_au >= 1.0, Threat Level is 'CRITICAL'.

            Return a structured markdown report containing:
            - Threat Level (LOW or CRITICAL)
            - Optical Fingerprint Analysis (UV/Vis/NIR findings)
            - Closed-Loop Remediation Action (Micro-solenoid dosing command)
            - Consumption Line Safety Lockout Status (Engaged or Disengaged)
            - Epidemiological Radar Network Dispatch Summary
            """
            
            response = client.chat.completions.create(
                model=model_name,
                temperature=0.0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Telemetry Data: {json.dumps(telemetry_payload)}"}
                ]
            )
            
            st.success("Live E-DSN Diagnostic Analysis Complete!")
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
