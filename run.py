from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
print(os.environ.get("OPENAI_API_KEY")) #key should now be available

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY"),
)