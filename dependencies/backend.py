
import requests
import json
import sys
import sqlite3
import os

def make_req(question):
    # Make the request
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer sk-or-v1-d96ab74e7dc20ac8fb9c198d3b54852639489c37d42cbee90c3beeb3ebfxxxxx",
            "Content-Type": "application/json",  # Important: Add this header
        },
        data=json.dumps({
            "model": "google/gemma-2-9b-it:free",  # Optional
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        })
    )

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Parse the JSON response
            data = response.json()
            
            # Extract the content safely
            if "choices" in data and len(data["choices"]) > 0:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "")
                
                if content:
                    return(content)
                else:
                    noCont = "No content in response"
                    return noCont
            else:
                return(data)
                
        except json.JSONDecodeError:
            print("Failed to parse JSON response")
            print("Raw response:", response.text)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Error response:", response.text)

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), '..', 'userChatRecords.db')
    
    aiUserID = -1
    question = sys.argv[1]
    chat_id = sys.argv[2]

    chat_id = int(chat_id)

    aiResponse = make_req(question)

    conn = sqlite3.connect('userChatRecords.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Messages (ChatID, UserID, MessageContent) 
    VALUES (?, ?, ?)
    ''', (chat_id, aiUserID , aiResponse))
    conn.commit()

    os._exit(0)
