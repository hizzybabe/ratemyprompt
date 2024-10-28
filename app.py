from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rate-prompt', methods=['POST'])
def rate_prompt():
    try:
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({
                'score': 0,
                'advice': 'Error: No prompt provided'
            }), 400
        
        # Analyze prompt using Gemini
        analysis_prompt = f"""
        Analyze the following prompt and provide two things:
        1. A score out of 100 based on clarity, specificity, and effectiveness
        2. Specific advice on how to improve the prompt

        Prompt to analyze: "{prompt}"

        Respond strictly in this JSON format:
        {{"score": <number>, "advice": "<string>"}}
        """
        
        response = model.generate_content(analysis_prompt)
        if not response.text:
            raise ValueError("Empty response from Gemini")
        
        # Clean and parse the response
        try:
            # Remove any potential markdown formatting or extra whitespace
            cleaned_text = response.text.strip().strip('`').strip()
            if cleaned_text.startswith('json'):
                cleaned_text = cleaned_text[4:].strip()
            
            import json
            result = json.loads(cleaned_text)
            
            # Validate the response format
            if not isinstance(result.get('score'), (int, float)) or not isinstance(result.get('advice'), str):
                raise ValueError("Invalid response format")
                
            return jsonify(result)
            
        except json.JSONDecodeError as e:
            return jsonify({
                'score': 0,
                'advice': f'Error parsing response: Invalid JSON format'
            }), 500
            
    except Exception as e:
        return jsonify({
            'score': 0,
            'advice': f'Error analyzing prompt: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
