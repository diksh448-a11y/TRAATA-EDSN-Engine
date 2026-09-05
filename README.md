# TRAATA - Distributed Environmental Disease Surveillance Node (E-DSN)

TRAATA is a split-architecture edge diagnostic platform designed for real-time domestic water contamination monitoring and automated prophylactic remediation[cite: 1].

## 📌 Core Features
* **Reagent-Free Optical Fingerprinting:** Multi-wavelength (UV/Vis/NIR) spectroscopic analysis detecting biological pathogen signatures without chemical sensor degradation[cite: 1].
* **Autonomous Anti-Biofouling:** Programmed 265nm UV-C LED pulses to scramble biofilm DNA, maintaining 24-month optical accuracy[cite: 1].
* **Closed-Loop Intervention:** Micro-solenoid valve integration for precision micro-dosing and automatic safety lockout line isolation during critical threats[cite: 1].
* **Epidemiological Radar Integration:** Decentralized node reporting sending real-time anomaly telemetry via MQTT to regional outbreak dashboards[cite: 1].

## 🛠️ Tech Stack
* **UI/Frontend:** Python, Streamlit
* **AI Analysis Engine:** OpenAI / Groq (Llama 3.3 70B / GPT-4o-mini)
* **Data Format:** Structured JSON Telemetry Payload

## 🚀 Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/diksh448-a11y/TRAATA-EDSN-Engine.git](https://github.com/diksh448-a11y/TRAATA-EDSN-Engine.git)
   cd TRAATA-EDSN-Engine
