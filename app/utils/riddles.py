from utils.config import llm_model
from utils.config import client

# Class to generate riddles

def generate_riddle() -> str:
    """
    Generate a riddle.
    """
    # Prompt the llm to generate a riddle
    prompt = "Generate a riddle."
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content