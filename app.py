from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS 
import openai
import os

app = Flask(__name__)
CORS(app) 

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("combined.txt", "r") as file:
    resume_data = file.read()

# POST endpoint for the chatbot (already exists)
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    try:
        prompt = f"MiLaDy documentation is given as follows:\n\n{resume_data}\n\nUser question: {user_message}\nAnswer:"
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an intelligent virtual assistant for the MiLaDy software. Your role is to help users understand and use MiLaDy by providing accurate, helpful answers based on the MiLaDy documentation. You should assist users in writing and configuring MiLaDy input files according to their specific needs. Always provide clear explanations, examples when relevant, and ensure your answers are consistent with the MiLaDy documentation. If the requested information is not available in the MiLaDy documentation, explicitly say that you don’t know rather than guessing or providing unrelated information."},
                {"role": "user", "content": prompt}
            ]
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": f"Error: {str(e)}"}), 500

# Frontend page accessible via GET
@app.route('/', methods=['GET'])
def home():
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MiLaDy Chatbot</title>
        <style>
            body { font-family: Calibri, sans-serif; max-width: 1000px; margin: 2em auto; }
            #chatbox { border: 1px solid #ccc; padding: 1em; height: 400px; overflow-y: auto; }
            #user-input { width: 80%; }
            button { width: 18%; ; font-size: 20px; padding: 10px 0; cursor: pointer; }
            .user-msg { color: #414345; margin: 0.5em 0; font-size: 20px;}
            .bot-msg { color: #003366; margin: 0.5em 0; white-space: pre-wrap; font-size: 20px;}
        </style>
    </head>
    <body>
        <h1>Ask anything about MiLaDy!</h1>
        <div id="chatbox"></div>
        <input type="text" id="user-input" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>

        <script>
            async function sendMessage() {
                const input = document.getElementById('user-input');
                const msg = input.value.trim();
                if(!msg) return;

                const chatbox = document.getElementById('chatbox');
                chatbox.innerHTML += '<div class="user-msg"><b>You:</b> ' + msg + '</div>';

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: msg })
                });
                const data = await response.json();
                chatbox.innerHTML += '<div class="bot-msg"><b>Bot:</b> ' + data.reply + '</div>';
                chatbox.scrollTop = chatbox.scrollHeight;
                input.value = '';
            }

            // Allow pressing Enter to send
            document.getElementById('user-input').addEventListener('keypress', function(e) {
                if(e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
