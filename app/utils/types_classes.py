from pydantic import BaseModel, Field


# define type for the return of the model once it chooses image
class ChosenObject(BaseModel):
    object: list[str] = Field("The object chosen from the image.")


# pydantic type to verify if the user's guess is correct or not
class GuessVerificationObject(BaseModel):
    correct: int = Field("States whether the guess is correct or not")
    model_output: str = Field("Returns in text whether the guess was correct or not")
    message: str = Field("Model message or hint.")


# Define the schema for the output
class ObjectToList(BaseModel):
    objects: list[str] = Field(description="The objects in the prompt. The format is: 'object1, object2, object3'")
    extra_words: int = Field(description="All other words in the prompt.")
