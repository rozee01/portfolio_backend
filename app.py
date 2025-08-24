from flask import Flask, request, jsonify, render_template
from graph import graph
from flask_cors import CORS
from conversation_store import  reset_history

app = Flask(__name__)
CORS(app)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question")
    thread_id = data.get("thread_id")

    if not question:
        return jsonify({"error": "Missing 'question'"}), 400

    state = {"thread_id": thread_id, "question": question}
    result = graph.invoke(state)

    return result["answer"]

@app.route("/reset", methods=["POST"])
def reset():
    data = request.get_json()
    thread_id = data.get("thread_id")
    reset_history(thread_id)
    return jsonify({"status": "reset"})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
