from together import Together
from keys import TOGETHER_AI
import os
import base64
from pydantic import BaseModel, Field


class ChosenObject(BaseModel):
    object: str = Field("The object chosen from the image.")


SystemPrompt = """
    You are an AI game engine. We are going to play 'I spy with my little eye'. 
    I will give you a list of images and you will have to choose an object you see in one of these images and return it to me. 
    In your response, you should only return the name of the object you see in the image. Try to keep the input limited to one word.
    """


def get_together_response(
        client: Together,
        images: list,
        model: str
) -> dict:
    content_list = [{"type": "text", "text": SystemPrompt}]

    for image in images:
        image_path = os.path.join("./test_images/", image)
        base64_image = encode_image_to_base64(image_path)
        content_list += [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]
    #content_list += [{"type": "image_url", "image_url": {"url": "./test_images/" + image}} for image in images] 
    #print(content_list)

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
    return response


def get_images(image_folder) -> list:
    # get images from the folder path
    image_list = [
        image for image in os.listdir(image_folder)
        if image.endswith(('.png', '.jpg', '.jpeg'))
    ]
    return image_list[1:2]


def encode_image_to_base64(image_path):
    """Convert an image to base64 encoding"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def verify_guess(
        client: Together,
        guess: str,
        model: str,
        chosen_object: str
):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"""
                    The object you chose is {chosen_object}. In your answer just return whether the guess is correct or not. 
                    If the guess is correct, return 'Correct!', if not, return 'Incorrect!'

                    Here is an example iteraction of the game:

                    Correct guess:
                        Chosen object: Bowl
                        User: Is the object you chose Bowl?
                        AI: Correct!
                    
                    Incorrect guess:
                        Chosen object: Bowl
                        User: Is the object you chose Cup?
                        AI: Incorrect!
                """
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Is the object you chose {guess}?"}
                ]
            }
        ],
        stream=True
    )
    return response


def main():
    client = Together(api_key=TOGETHER_AI)

    image_list = get_images("./test_images/")
    #response = get_together_response(client, image_list, "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo")
    chosen_object = None

    try:
        response = get_together_response(client, image_list, "Qwen/Qwen2.5-VL-72B-Instruct")

        chosen_object = eval(response.choices[0].message.content)

        for chunk in response:
            if hasattr(chunk.choices[0].delta, 'content'):
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
        print()
    except Exception as e:
        print()

    # begin guessing
    finished = False
    while not finished:
        user_input = input("\nGuess the object: ")
        try:
            response = verify_guess(client, user_input, "Qwen/Qwen2.5-VL-72B-Instruct", chosen_object["object"])

            for chunk in response:
                if hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content:
                        print(content, end="", flush=True)
                        if "Correct" in content:
                            finished = True
            print()
        except IndexError as e:
            pass

    print("\nGame over!")


if __name__ == "__main__":
    main()
