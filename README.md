# 🌾 Smart Krishi Coach

Smart Krishi Coach is a farmer-centric web application designed to assist **Andhra Pradesh (AP) farmers** in making **scientific, data-driven irrigation decisions**.  
The system generates a clear **7-day irrigation schedule** by analyzing crop type, soil condition, growth stage, location, and environmental factors.

This project focuses on **practical usability**, **local language accessibility**, and **sustainable water management**.

---

## 📌 Project Motivation

Traditional irrigation practices often rely on experience and guesswork, which can lead to:
- Over-irrigation or under-irrigation
- Water wastage
- Reduced crop productivity
- Poor adaptation to rainfall conditions

Smart Krishi Coach addresses these challenges by providing **rule-based, science-backed irrigation guidance** that is simple, fast, and farmer-friendly.

---

## 🎯 Key Objectives

- Provide accurate **7-day irrigation recommendations**
- Reduce water wastage using rain and soil logic
- Support **Telugu language** for easy adoption
- Offer a **mobile-first, easy-to-use interface**
- Enable farmers to make confident irrigation decisions

---

## ⚙️ System Overview

The application collects essential agricultural inputs from the user and processes them through a **rule-based irrigation engine** to determine whether irrigation is required or should be avoided.

### Decision indicators are displayed using:
- 🔴 **RED** – Skip irrigation (high rain probability)
- 🟡 **YELLOW** – No irrigation (soil already wet)
- 🟢 **GREEN** – Irrigation required

---

## 🔧 Inputs Required

1. **Crop Selection**  
   - 15+ supported crops  
   - Examples:  
     - Paddy (వరి)  
     - Cotton (పత్తి)  
     - Maize (మొక్కజొన్న)  
     - Groundnut (వేరుసెనగ)

2. **Soil Type**  
   - Light Soil  
   - Heavy Soil  
   - Red Soil  
   - Black Soil  
   - (with Telugu names)

3. **Location**  
   - 18 Andhra Pradesh districts  
   - Range: Bhimavaram → Visakhapatnam (Vizag)

4. **Last Irrigation Date**

5. **Crop Growth Stage**  
   - Nursery  
   - Early Growth  
   - Vegetative  
   - Flowering  
   - Grain/Fruit Formation  
   - Maturity

6. **Sensor Mode**  
   - IoT Simulation: ON / OFF

---

## 💧 Irrigation Decision Logic

| Condition | Action |
|---------|--------|
| Rain probability ≥ 70% | Skip irrigation |
| Soil moisture > 45% | Do not irrigate |
| Irrigation interval due | Irrigate once |

---

## 🧑‍🌾 Farmer Benefits

- ✔ Clear **7-day irrigation plan**
- ✔ Reduced dependency on guesswork
- ✔ **Water-efficient irrigation**
- ✔ Telugu language support for rural users
- ✔ Color-coded recommendations for quick understanding
- ✔ Mobile-friendly design for field usage

---

## 🛠️ Technology Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Logic Engine:** Rule-based agricultural decision system
- **UI Design:** Mobile-first responsive interface
- **Language Support:** Telugu & English

---

## 📂 Project Structure

smart_krishi_coach/
│── app.py
│── logic.py
│── requirements.txt
│
├── data/
│ └── crop_rules.json
│
├── templates/
│ └── index.html
│
└── static/
├── style.css
└── script.js

---

## ▶️ How to Run the Project Locally

1. Install **Python 3.8 or above**
2. Clone the repository:
   ```bash
   git clone https://github.com/NandikaHasini/smart_krishi_coach.git
RUN:
cd smart_krishi_coach
pip install -r requirements.txt
python app.py
http://127.0.0.1:5000/

🚀 Future Enhancements

1.Integration with live weather APIs
2.Machine learning based yield prediction
3.Real IoT sensor integration
4.Telugu voice input for farmers
5.WhatsApp alert system for irrigation reminders
