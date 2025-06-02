from flask import Flask, request, jsonify, render_template
from agents import orchestrator

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()
    history = data.get("history", [])

    if not question:
        return jsonify({"error": "Missing question field."}), 400

    response, agent = orchestrator(question, history)

    return jsonify({"response": response, "agent": agent})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
