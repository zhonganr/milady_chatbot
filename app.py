from flask import Flask, request, jsonify
from flask_cors import CORS 
import openai
import os

app = Flask(__name__)
CORS(app) 

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("combined.txt", "r") as file:
    resume_data = file.read()


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    try:
        prompt = f"MiLaDy documentation is given as follows:\n\n{resume_data}\n\nUser question: {user_message}\nAnswer:"

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are an intelligent virtual assistant for the MiLaDy software. Your role is to help users understand and use MiLaDy by providing accurate, helpful answers based on the MiLaDy documentation. You should assist users in writing and configuring MiLaDy input files according to their specific simulation or research needs. Always provide clear explanations, examples when relevant, and ensure your answers are consistent with the MiLaDy documentation. If the requested information is not available in the MiLaDy documentation, explicitly say that you don’t know rather than guessing or providing unrelated information."},
                      {"role": "user", "content": prompt}]
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
