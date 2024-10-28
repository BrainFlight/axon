# import openai
# import speech_recognition as sr
# from flask import Flask, request, jsonify

# from .constants import E7_V1_XRIF_PROMPT
# from .proompt_eng import chain_of_thought_v1

# # Initialize the Flask app
# app = Flask(__name__)

# # Set up your OpenAI API key
# openai.api_key = 'your-openai-api-key-here'

# # Function to capture microphone input and convert to text
# def get_microphone_input():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = recognizer.listen(source)

#         try:
#             print("Recognizing...")
#             text = recognizer.recognize_google(audio)
#             print(f"Recognized Text: {text}")
#             return text
#         except sr.UnknownValueError:
#             return "Could not understand audio"
#         except sr.RequestError as e:
#             return f"Could not request results; {e}"

# # Function to interact with OpenAI API
# def query_openai(prompt):
#     try:
#         response = openai.Completion.create(
#             engine="gpt-4",
#             prompt=prompt,
#             max_tokens=100,
#             n=1,
#             stop=None,
#             temperature=0.5,
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         return f"Error querying OpenAI API: {e}"

# @app.route('/speech_to_prompt', methods=['GET'])
# def speech_to_prompt():
#     text_from_microphone = get_microphone_input()

#     if not text_from_microphone or "Could not" in text_from_microphone:
#         return jsonify({"error": "Failed to recognize speech"}), 400

#     gpt_response = query_openai(chain_of_thought_v1(E7_V1_XRIF_PROMPT, text_from_microphone))

#     return jsonify({"prompt": text_from_microphone, "response": gpt_response})

# @app.route('/speech_to_prompt', methods=['POST'])
# def text_prompt():
#     req_text = request.json.get("text")
#     gpt_response = query_openai(chain_of_thought_v1(E7_V1_XRIF_PROMPT, req_text))
#     return jsonify({"prompt": req_text, "response": gpt_response})


# if __name__ == '__main__':
#     app.run(debug=True)

import os

import speech_recognition as sr
# import openai
# from dotenv import load_dotenv

from constants import E7_V1_XRIF_PROMPT
from proompt_eng import chain_of_thought_v1

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

def listen_to_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now!")
        audio = recognizer.listen(source)
    return audio

def convert_speech_to_text(audio):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def send_to_gpt4(text):
    try:
        print(text)
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": text}
        #     ]
        # )
        # return response.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI API: {e}")
        return None

def main():
    while True:
        audio = listen_to_microphone()
        text = convert_speech_to_text(audio)
        
        if text:
            print("Sending to GPT-4...")
            response = send_to_gpt4(text)
            if response:
                print(f"GPT-4 response: {response}")
        
        choice = input("Do you want to continue? (y/n): ").lower()
        if choice != 'y':
            break

if __name__ == "__main__":
    main()
