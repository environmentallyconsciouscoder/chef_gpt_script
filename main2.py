from openai import OpenAI
import os

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

personality = "You are an old and experienced chef who served in army for many years. You can be rude sometimes, and critical. You try to cook things fast, but they should be high in protein and calories. You alwats want food to be tasty and energetic."

messages = [
    {
        "role": "system",
        "content": personality
    }
]

messages.append(
     {
          "role": "system",
          "content": "If your client is going to ask for a recipe about a specific dish e.g. create a dish using these ingredients. Then give name of a dish only no recipe. If your client is asking for suggestion for a dish using thier recipes e.g. suggest me a detailed recipe and the preparation steps for making. Then you will give recipe and instructions. If your client is asking for feedback on their recipes. e.g. give me feedback on my recipes. Then you will give feedback only no recipe. If the user passes a different prompt than these three scenarios as the first message, then you should deny the request and ask to try again."
     }
)

model = "gpt-3.5-turbo"

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

print("Hello, this is Chef!")
print("You can ask following type of question: \n Ask what to cook from what you have; \n Ask a detailed recipe and the preparation steps for making dish; \n Ask for feedback, on your food and recipes")
print("Enjoy the chat! (to finish chat type \'FINISH\')\n")


collected_messages = []
while True:
    print("\n")
    user_input = input("How can I help you?\n")
    if user_input.strip().lower() == "finish":
        print("The chat ended")
        break
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )
