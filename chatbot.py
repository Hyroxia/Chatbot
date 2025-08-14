import google.generativeai as genai

#api key
API_KEY = "AIzaSyCppZRLDk2u8fM1HR5MCmzwTOpr326ULT8"

# placeing the api key in the configure api key
genai.configure(api_key=API_KEY)

#create a variable for genai
model = genai.GenerativeModel("gemini-pro")

#display messages
print("Gemini Chatbot (type 'quit' to exit)")
print("-----------------------------------")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["quit", "exit"]:
        print("Bot: Goodbye!")
        break

    try:
        response = model.generate_content(user_input)
        print("Bot:", response.text.strip())
    except Exception as e:
        print("Bot: Error -", str(e))