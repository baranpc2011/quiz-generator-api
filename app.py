import os

from flask import Flask, request, jsonify
from quiz_generator import generate_questions
app = Flask(__name__)

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()

    story = data.get('story')
    question_count = data.get('question_count')

    # TODO: validation — what if story or question_count is missing/invalid?
    if not story or not question_count:
        return jsonify({"error": "Missing required fields"}), 400

    # TODO: call generate_questions(story, question_count)
    questions = generate_questions(story, question_count)

    if questions is None:
        return jsonify({"error": "Failed to generate questions"}), 500

    # but Groq's output won't include that — you'll need to add it yourself.
    # hint: loop over the questions with enumerate() to get an index + the question together

    # TODO: build and return the final response matching the assignment's exact shape:
    # {"total_questions": ..., "questions": [...]}
    return jsonify({
        "total_questions": len(questions),
        "questions": questions
    })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host='0.0.0.0', port=port)