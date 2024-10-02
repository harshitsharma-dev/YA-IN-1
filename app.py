from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

# Initialize the Flask application
app = Flask(__name__)

# Initialize the Groq client with the provided API key
client = Groq(api_key="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")

def validate_question(question):
    """Check if the question is related to water and sanitation infrastructure pricing."""
    valid_keywords = [
        'water', 'sanitation', 'infrastructure', 'pricing', 'cost',
        'pipes', 'treatment', 'purification', 'sewage', 'wastewater',
        'pricing models', 'distribution', 'systems'
    ]
    # Return True if the question contains any of the valid keywords
    return any(keyword in question.lower() for keyword in valid_keywords)

def query_groq(question):
    """Query Groq Llama3-8b for a response related to water and sanitation infrastructure pricing."""
    # Validate if the question is within the specified domain
    if validate_question(question):
        # Add specific instructions in the system prompt
        messages = [
            {
                "role": "system",
                "content": "You are an expert in water and sanitation infrastructure pricing. Only respond to questions which are relevant to this domain little bit or in some way. If the question is highly out of scope, respond with 'I only answer questions related to water and sanitation infrastructure pricing.'"
            },
            {
                "role": "user",
                "content": question
            }
        ]

        # Create a chat completion with Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
        )

        # Return the generated response
        return chat_completion.choices[0].message.content

    # If the question is not valid, return a rejection message
    return "I only answer questions related to water and sanitation infrastructure pricing."

# Routes to Render Pages

@app.route('/')
def index():
    return render_template('index.html')  # Render index.html as the homepage

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/bids')
def bids():
    return render_template('bids.html')

@app.route('/Finances')
def finances():
    return render_template('finances.html')

@app.route('/audit')
def audit():
    return render_template('audit.html')

# Chatbot API Endpoint
@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_question = request.form['question']
        response = query_groq(user_question)
        return jsonify(response=response)
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify(response="Sorry, there was an error processing your request."), 500

# Run the Flask Application
if __name__ == "__main__":
    app.run(debug=True)
