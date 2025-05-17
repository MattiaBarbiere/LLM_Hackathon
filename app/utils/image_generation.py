import base64
from io import BytesIO
from PIL import Image
from utils.config import client

def generate_hangman_image() -> str:
    """
    Generate an image of a hangman game.
    """
    hangman = "Mr. Incredible"
    current_number_guess = 5
    prompt = f"I am playing a game of hangman. You need to draw the hangman" \
    f" the parts of the hand are the pole, the beem the rope. Then the head, the body, left arm, right arm, left leg, right leg."\
    f"The person to be hanged is {hangman}. The player has guessed {current_number_guess} number of times. You must " \
    f" draw the hangman with the parts equal to the number fo guresses."
    
    
    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell",
        steps=10,
        n=4
    )
    print("\nimage url : ", response.data[0].url)