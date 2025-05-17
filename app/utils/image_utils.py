import os
import base64


def delete_saved_photos():
    """
    Deletes all saved photos in the app/saved_photos directory.
    """
    for file in os.listdir("app/saved_photos"):
            if file.endswith(".jpg") or file.endswith(".png"):
                os.remove(os.path.join("app/saved_photos", file))

def encode_image_to_base64(image_path):
    """Convert an image to base64 encoding"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')