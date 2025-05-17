import json
import os

from utils.config import *
from utils.image_utils import encode_image_to_base64
from utils.types_classes import (
    ChosenObject,
    GuessVerificationObject
)


def query_llm(input_text, user_id):
    if user_id not in N_WORDS:
        N_WORDS[user_id] = -1

    if N_WORDS[user_id] > 0:
        input_text += f" (in {N_WORDS[user_id]} words or less)"

    # add to message history
    if user_id in USER_MESSAGES:
        USER_MESSAGES[user_id].append({"role": "user", "content": input_text})
    else:
        USER_MESSAGES[user_id] = [
            {"role": "system",
             "content": "You are a witty, annoyed pissed off assistant, always trying to find a way to insult the user."},
            {"role": "user", "content": input_text}
        ]

    # prompt LLM
    response = client.chat.completions.create(
        model=llm_model,
        messages=USER_MESSAGES[user_id]
    )
    text_response = response.choices[0].message.content

    # update message history
    USER_MESSAGES[user_id].append({"role": "assistant", "content": text_response})

    if VERBOSE:
        print(USER_MESSAGES[user_id])

    # clear chat history (if too long)
    if len(USER_MESSAGES[user_id]) > 2 * MAX_CHAT_HISTORY:
        # remove bot response
        USER_MESSAGES[user_id].pop(0)
        # remove question
        USER_MESSAGES[user_id].pop(0)

    text_response = f"MODEL: {llm_model}\n\n{text_response}"
    # truncate response if too long
    if len(text_response) > TELEGRAM_MAX_OUTPUT:
        text_response = text_response[:TELEGRAM_MAX_OUTPUT - 20] + "\n\nOUTPUT TRUNCATED"
    return text_response


def generate_image(prompt, user_id):
    """
    Generate an image based on a text prompt using Together AI.

    Args:
        prompt (str): The text description of the image to generate
        user_id (str): The user ID for tracking requests

    Returns:
        tuple: (success, result) where result is either the image URL or an error message
    """
    try:
        # Generate the image
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell",
            steps=4,
            disable_safety_checker=True
        )

        # Get the image URL from the response
        image_url = response.data[0].url

        if VERBOSE:
            print(f"Generated image for user {user_id}: {image_url}")

        return True, image_url

    except Exception as e:
        error_msg = f"Error generating image: {str(e)}"
        print(error_msg)
        return False, error_msg


def choose_object(
        image_path: list,
        model: str
) -> dict:
    SystemPrompt = """
        You are an AI game engine. We are going to play 'I spy with my little eye'. 
        I will give you a list of images and you will have to choose an object you see in one of these images and return it to me. 
        In your response, you should only return the name of the object you see in the image. Try to keep the input limited to one word.
    """

    content_list = [{"type": "text", "text": SystemPrompt}]

    base64_image = encode_image_to_base64(image_path)
    content_list += [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": content_list
            }],
        response_format={
            "type": "json_object",
            "schema": ChosenObject.model_json_schema()
        }
    )
    return json.loads(response.choices[0].message.content)


def verify_guess(
        guess: str,
        chosen_object: str
):
    print(guess, chosen_object)
    response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
                "role": "system",
                "content": f"""
                    The object I chose is {chosen_object}. In your answer just return whether the guess is correct or not. 
                    If the guess is correct, return 1 in the correct field and 'Correct!' in the model_output field. 
                    If not, return 0 and 'Incorrect!'
                    If the user input is wrong, return a hint.

                    Here is an example iteraction of the game:

                    Correct guess:
                        Chosen object: Bowl
                        User: Is the object you chose Bowl?
                        AI: 
                            'correct': 'True',
                            'model_output': 'Correct!'
                            'message': 'Congratulations, you guessed correctly!'
                        
                    
                    Incorrect guess:
                        Chosen object: Bowl
                        User: Is the object you chose Cup?
                        AI: 
                            'correct': 'False',
                            'model_output': 'Incorrect!'
                            'message': 'Hhhm, your guess is not correct. You would use this to object eat not drink...'
                """
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Is the object you chose {guess}?"}
                ]
            }
        ],
        response_format={
            "type": "json_object",
            "schema": GuessVerificationObject.model_json_schema()
        }
    )
    return json.loads(response.choices[0].message.content)
