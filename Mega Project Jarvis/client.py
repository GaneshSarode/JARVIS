from openai import OpenAI
import os
client = OpenAI(api_key=os.environ.get("CUSTOM_ENV_NAME"),)