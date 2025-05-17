import os

def delete_saved_photos():
    """
    Deletes all saved photos in the app/saved_photos directory.
    """
    for file in os.listdir("app/saved_photos"):
            if file.endswith(".jpg") or file.endswith(".png"):
                os.remove(os.path.join("app/saved_photos", file))