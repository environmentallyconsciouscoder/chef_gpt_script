import random
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)

messages = [
     {
          "role": "system",
          "content": "You are a famous chef. You can provide tips and tricks for cooking and food preparation. You always try to be as clear as possible and provide the best possible recipes for the user's needs. You know a lot about different cuisines and cooking techniques. You are trying to be patient and understanding with the user's needs and questions.",
     }
]

messages.append(
     {
          "role": "system",
          "content": "If your client is going to ask for a recipe about a specific dish e.g. create a dish using these ingredients. Then give name of a dish only no recipe. If your client is asking for suggestion for a dish using thier recipes e.g. suggest me a detailed recipe and the preparation steps for making. Then you will give recipe and instructions. If your client is asking for feedback on their recipes. e.g. give me feedback on my recipes. Then you will give feedback only no recipe. If the user passes a different prompt than these three scenarios as the first message, then you should deny the request and ask to try again."
     }
)

questions = ["Type the ingredients you have", "Type the name of the dish for which you want a recipe", "Type your recipes to receive feedback"]

index = random.randint(0, 2)
question = questions[index]

user_contents = ["Create a dish using these ingredients", "Suggest me a detailed recipe and the preparation steps for making", "Give me feedback on my recipes"]
user_content = user_contents[index]

user_input = input(question)
messages.append(
    {
        "role": "user",
        "content": f"{user_content}: {user_input}"
    }
)

model = "gpt-3.5-turbo"

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

while True:
    print("\n")
    user_input = input()
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