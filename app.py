from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "The 'question' field is required."}), 400

    # Example answer logic (to be improved with scraped content)
    if "gpt-4o-mini" in question.lower():
        answer_text = "You must use `gpt-3.5-turbo-0125`, even if the AI Proxy only supports `gpt-4o-mini`. Use the OpenAI API directly for this question."
        links = [
            {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4", "text": "Use the model that’s mentioned in the question."},
            {"url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3", "text": "My understanding is that you just have to use a tokenizer, similar to what Prof. Anand used, to get the number of tokens and multiply that by the given rate."}
        ]
    else:
        answer_text = "I recommend checking course content and previous discussions for clarification."
        links = []

    return jsonify({"answer": answer_text, "links": links})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)