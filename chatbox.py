import json
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def ask(prompt, history):
    history.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        max_tokens=200,
        temperature=0.7,
    )

    text = completion.choices[0].message.content
    history.append({"role": "assistant", "content": text})

    return text, history

print("Chatbot, write 'exit' to quit")

history = [
    {"role": "system", "content": "Jsi vtipný český chatbot, co mluví neformálně a říká občas vtípky. Hodně ironický."}
]
while True:
    prompt = input("You: ")
    if prompt.lower() == "exit":
        break

    response, history = ask(prompt, history)
    print("Bot:", response)    

if len(history) > 10:
    history = history[-10:]     