from pydantic import BaseModel, Field

# define type for the return of the model once it chooses image
class ChosenObject(BaseModel):
    object: str = Field("The object chosen from the image.")

# pydantic type to verify if the user's guess is correct or not
class GuessVerificationObject(BaseModel):
    correct: int = Field("States whether the guess is correct or not")
    model_output: str = Field("Returns in text whether the guess was correct or not")
    message: str = Field("Model message or hint.")