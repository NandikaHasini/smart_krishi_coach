import json
from datetime import datetime, timedelta
from pathlib import Path

# ---------- Load crop rules from JSON ----------

DATA_DIR = Path(__file__).parent / "data"
RULES_PATH = DATA_DIR / "crop_rules.json"

with open(RULES_PATH, "r") as f:
    CROP_RULES = json.load(f)


def get_base_interval(crop: str, soil: str) -> int:
    """
    Return base irrigation interval in days for given crop & soil.
    Falls back to 5 days if something is missing.
    """
    crop = (crop or "").lower()
    soil = (soil or "").lower()
    return CROP_RULES.get(crop, {}).get(soil, 5)


def get_dummy_weather_profile(location: str):
    """
    Return a list of 7 dicts with simple dummy weather data.
    Each item: {"rain_prob": int, "temp": int}
    """
    # Example pattern: some medium, some high rain days
    base_temps = [30, 31, 32, 29, 28, 33, 34]
    rain_probs = [20, 40, 70, 10, 50, 80, 30]

    profile = []
    for i in range(7):
        profile.append({
            "rain_prob": rain_probs[i],
            "temp": base_temps[i]
        })
    return profile


# ---------- IoT simulation: virtual soil moisture ----------

def get_virtual_soil_moisture(day_index: int) -> int:
    """
    Very simple virtual soil moisture pattern (in %).
    Starts wetter and gradually dries over the week.
    """
    base = 70 - day_index * 6  # 70%, 64%, 58%, ...
    return max(15, base)


def generate_plan(
    crop: str,
    soil: str,
    location: str,
    last_irrigation_str: str,
    sensor_mode: str = "off"
):
    """
    Build 7-day irrigation plan.

    last_irrigation_str: 'YYYY-MM-DD'
    sensor_mode: 'on' or 'off'
    Returns list of 7 dicts:
    {
        day, date, action, reason, color, rain_prob, soil_moisture
    }
    """
    base_interval = get_base_interval(crop, soil)
    weather = get_dummy_weather_profile(location)

    last_irrigation = datetime.strptime(last_irrigation_str, "%Y-%m-%d").date()
    today = datetime.today().date()

    plan = []

    for i in range(7):
        current_date = today + timedelta(days=i)
        days_since_irrigation = (current_date - last_irrigation).days

        rain_prob = weather[i]["rain_prob"]
        moisture = get_virtual_soil_moisture(i) if sensor_mode == "on" else None

        # --- Decision logic ---

        # 1) Rain override
        if rain_prob >= 70:
            action = "Skip irrigation"
            reason = (
                f"High chance of rain ({rain_prob}%). "
                "Let rainfall provide water and avoid wastage."
            )
            color = "red"

        # 2) Sensor-based override in IoT mode
        elif sensor_mode == "on" and moisture is not None and moisture > 45:
            action = "No irrigation"
            reason = (
                f"Virtual soil moisture is {moisture}%. Field is still wet; "
                "delay irrigation to save water."
            )
            color = "yellow"

        # 3) Interval reached: irrigate
        elif days_since_irrigation >= base_interval:
            action = "Irrigate once"
            reason = (
                f"{days_since_irrigation} days since last irrigation, "
                f"which meets the {base_interval}-day interval for {crop} on {soil} soil."
            )
            color = "green"
            last_irrigation = current_date

        # 4) Otherwise: no irrigation
        else:
            action = "No irrigation"
            reason = (
                f"Only {days_since_irrigation} days since last irrigation; "
                "soil likely still has sufficient moisture."
            )
            color = "yellow"

        plan.append({
            "day": f"Day {i + 1}",
            "date": current_date.isoformat(),
            "action": action,
            "reason": reason,
            "color": color,
            "rain_prob": rain_prob,
            "soil_moisture": moisture
        })

    return plan


# ---------- Simple FAQ / chat logic ----------

FAQ_ANSWERS = {
    "irrigation": (
        "Smart Krishi Coach schedules irrigation based on crop, soil type and days since last "
        "watering. In sensor mode, it also looks at soil moisture: if the field is still wet, "
        "it delays irrigation to save water."
    ),
    "fertilizer": (
        "This demo focuses on water decisions. As a thumb rule, avoid applying fertilizers just "
        "before heavy rain to reduce nutrient loss and runoff risk."
    ),
    "spray": (
        "Avoid spraying pesticides or fungicides when rain probability is high or winds are strong, "
        "to prevent wash-off and drift and to improve effectiveness."
    )
}


def answer_question(text: str) -> str:
    """
    Very simple intent-based QA for the mini chat.
    """
    text_l = (text or "").lower()

    if any(word in text_l for word in ["water", "irrigation", "neellu", "irigate", "irrigate"]):
        return FAQ_ANSWERS["irrigation"]

    if any(word in text_l for word in ["fertilizer", "urea", "dap", "manure"]):
        return FAQ_ANSWERS["fertilizer"]

    if any(word in text_l for word in ["spray", "pesticide", "fungicide", "spraying"]):
        return FAQ_ANSWERS["spray"]

    return (
        "Smart Krishi Coach currently answers basic queries on irrigation, fertilizer timing "
        "and spraying conditions. Please ask about these topics."
    )
