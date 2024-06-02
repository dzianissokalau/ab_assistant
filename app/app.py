from flask import Flask, request, jsonify, render_template
from openai import OpenAI

import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Define the model to use
MODEL = 'gpt-3.5-turbo' # 'gpt-4'

def create_messages(question):
    return [
        {"role": "system", "content": "You are an expert in A/B testing and experiment design."},
        {"role": "user", "content": question}
    ]


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/advice', methods=['POST'])
def get_advice():
    data = request.json
    question = data.get('question')
    if question:
        messages = create_messages(question)
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        print(response.choices[0].message.content)
        return jsonify(response.choices[0].message.content.strip())
    else:
        return jsonify({"error": "No question provided"}), 400

if __name__ == '__main__':
    app.run()
