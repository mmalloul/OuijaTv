import os
import openai
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

dotenv_path = Path('..env')

openai.api_key = os.getenv('API_KEY_OPENAI')

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are a ouija response bot that takes a question in a fills the blank that is ... your personality is that you are funny and dark the reponse must be really short"},
        {"role": "system", "content": "A bird is a ..."}

    ],
    n = 1,
    temperature = 0.8,
    max_tokens = 30,

)

print(completion.choices[0].message)

print('=======================')

print(completion)