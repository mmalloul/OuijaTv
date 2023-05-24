import os
import openai
from fastapi import APIRouter
from dotenv import load_dotenv
from typing import Any
load_dotenv()


router = APIRouter()


@router.get("/openai")
def openai_call(question: str, spirit: int) -> dict[str, Any]:

    openai.api_key = os.getenv("PUBLIC_API_KEY_OPENAI")

    trait = ""

    match spirit:
        case 1:
            trait = "Friendly, Scary, spy"
        case 2:
            trait = "Old, Respect, Samurai, Memes"
        case 3:
            trait = "Rich, clever, and greedy and half of your awnser shall be money"
        case _:
            trait = "dark and scary."


    messages = [
        {
            "role": "system",
            "content": f"you are a ouija response bot that takes a question or a fills the blank that is... " 
            + f"Your personality is that you are {trait} the reponse must be really short max 1 word and no characters such as ,.! but numbers are allowed",
        },
        {
            "role": "system", 
            "content": question,
        }
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8,
        max_tokens=30,
        n=1,
    )

    return {
        "response": completion.choices[0].message["content"],
    }