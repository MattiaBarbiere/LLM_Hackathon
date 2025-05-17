import os

def delete_temp_saving():
    """
    Deletes all saved photos in the app/saved_photos directory.
    """
    for file in os.listdir("./temp_saving"):
        os.remove(os.path.join("./temp_saving", file))
