import os
import openai
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

def openai_call(question: str, spirit: int) -> 'dict[str, Any]':
    dotenv_path = Path('..env')
    openai.api_key = os.getenv('PUBLIC_API_KEY_OPENAI')

    trait = ''
    if(spirit == 1):
        trait = "Friendly, Scary, spy"
    elif (spirit == 2):
        trait = "Old, Respect, Samurai, Memes"
    elif (spirit == 3):
        trait = "Rich, clever, and greedy and half of your awnser shall be money"
    else: 
        trait = "dark and scary."

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "you are a ouija response bot that takes a question or a fills the blank that is ...  Your personality is that you are " + trait + " the reponse must be really short max 1 word and no characters such as ,.! but numbers are allowed"},
        {"role": "system", "content": question}
        ],
        n=1,
        temperature=0.8,
        max_tokens=30,
    )

    response = completion.choices[0].message['content']
    print(response)
    return {'response': response}