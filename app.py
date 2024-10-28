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
        
        Format your response as JSON with 'score' and 'advice' keys.
        """
        
        response = model.generate_content(analysis_prompt)
        if not response.text:
            raise ValueError("Empty response from Gemini")
            
        result = eval(response.text)  # Note: Consider using json.loads() instead of eval()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'score': 0,
            'advice': f'Error analyzing prompt: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
