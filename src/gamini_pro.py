import requests
import json

API_KEY = "AIzaSyB3cH84Hio1m-0q8Gru0PZyyqguHkP3cGU"

def generate_response(question):
    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=" + API_KEY

        headers = {'Content-Type': 'application/json'}

        data = {
            "contents": [
                
                {
                    "role": "model",
                    "parts": [{"text": """I generate scientific article based on your code. I generate an article as formal as scientific. 
                               It generate an article with 
Abstact
Introduction
3 main paragraphs (based on your code, I will name for each of them)
Conclusion 
                               
Please send a code and I will make an article for you. In next respond you can get your article.
                               """}]
                }
                ,
                {
                    "role": "user",
                    "parts": [{"text": question}]
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        generated_respond = response.json()['candidates'][0]['content']['parts'][0]['text']

        return generated_respond
    except Exception as e:
        print(e)
        print(response.json())
        return 'Something went wrong. Please try again'