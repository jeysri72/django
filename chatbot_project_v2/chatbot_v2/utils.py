import requests
import os
from dotenv import load_dotenv
import markdown

# Load environment variables
load_dotenv()


def get_gemini_response(user_message):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + os.getenv('GEMINI_API_KEY')
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "contents": [
            {
                "parts":[
                    {
                        "text": user_message
                    }
                ]
            }
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    return response_data['candidates'][0]['content']['parts'][0]['text']

def convert_markdown_to_html(markdown_text):
    """Convert Markdown text to HTML."""
    html = markdown.markdown(markdown_text)
    return html

