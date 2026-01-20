from flask import Flask, render_template, request, jsonify
from logic import generate_plan, answer_question

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/plan", methods=["POST"])
def plan():
    """
    Receive farm details from frontend and return 7-day plan as JSON.
    """
    data = request.get_json()
    crop = data.get("crop")
    soil = data.get("soil")
    location = data.get("location")
    last_irrigation = data.get("last_irrigation")
    sensor_mode = data.get("sensor_mode", "off")

    if not all([crop, soil, location, last_irrigation]):
        return jsonify({"error": "Missing fields"}), 400

    plan_data = generate_plan(crop, soil, location, last_irrigation, sensor_mode)
    return jsonify(plan_data)


@app.route("/ask", methods=["POST"])
def ask():
    """
    Receive a question string and return a simple advisory answer.
    """
    data = request.get_json()
    question = data.get("question", "")
    answer = answer_question(question)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=True)
