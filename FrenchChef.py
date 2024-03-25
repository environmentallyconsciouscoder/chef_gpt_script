#Critical French chef
client = OpenAI(
         api_key=os.environ['OPENAI_API_KEY'],
     )
messages = [
        {
             "role": "system",
             "content": "You are a captious and impatient chef with 30 years of experience in french dishes. You provide recipes for dishes people want to cook. You can also provide tips and tricks for cooking the meal.",
        }
   ]

user_contents = input("What can I help you with? dish, recipe or review :\n")
if user_contents == "dish":
  """ Creates a dish from user's input """
  ingredients = input("What ingredients do you have? :\n")
  messages.append(
      {
          "role":"user",
          "content": f"Suggest a dish that can be made from these {ingredients}"
      }
  )

  messages.append(
        {
             "role": "system",
             "content": "Your client is going to give a list of ingredients, if there is only 1 ingredient, ask the user to try again. Provide a dish name (only)",
        }
   )
elif user_contents == "recipe":
  """ Generates a recipe for the user"""
  dish = input("Type the name of the dish you want a recipe for:\n")
  messages.append(
          {
              "role": "user",
              "content": f"Suggest me a detailed recipe and the preparation steps for making {dish}"
          }
      )

  messages.append(
        {
             "role": "system",
             "content": "Your client is going to ask for a recipe about a specific dish. If you do not recognize the dish, you should not try to generate a recipe for it. Do not answer a recipe if you do not understand the name of the dish.",
        }
   )

elif user_contents == "review":
  """ Reviews the users recipe and provides feedback """
  recipe = input("Type what recipe you want to make:\n")
  messages.append(
      {
          "role":"user",
          "content": f"Give feedback on {recipe} and suggest 1 improvement"
      }
  )

  messages.append(
        {
             "role": "system",
             "content": "Your client is going to give a recipe, critically assess the recipe and suggest an improvement. If there are no improvements, say: "great work". ",
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
