import os
import json
import tempfile
from flask import Flask, request, jsonify, send_file
from quiz_generator import generate_questions

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()

    story = data.get('story')
    question_count = data.get('question_count')

    if not story or not question_count:
        return jsonify({"error": "Missing required fields"}), 400

    questions = generate_questions(story, question_count)

    if not questions:
        return jsonify({"error": "Failed to generate questions"}), 500

    return jsonify({
        "total_questions": len(questions),
        "questions": questions
    })

@app.route('/api/download-quiz', methods=['POST'])
def download_quiz():
    data = request.get_json()

    story = data.get('story')
    question_count = data.get('question_count')

    if not story or not question_count:
        return jsonify({"error": "Missing required fields"}), 400

    questions = generate_questions(story, question_count)

    if not questions:
        return jsonify({"error": "Failed to generate questions"}), 500

    js_content = "const questions = " + json.dumps(questions, indent=2) + ";"

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".js", mode='w')
    tmp.write(js_content)
    tmp.close()

    return send_file(tmp.name, as_attachment=True, download_name="quiz.js")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host='0.0.0.0', port=port)