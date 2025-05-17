import json
from pydantic import BaseModel, Field
from utils.config import client

# Define the schema for the output
class ImageDescription(BaseModel):
    objects: list[str] = Field(description="The objects in the prompt. The format is: 'object1, object2, object3'")
    extra_words: int = Field(description="All other words in the prompt.")

def llm_objects_from_text(input_text: str,
                        # model: str = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
                        model: str = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
                        ) -> list:
    """
    Ask the LLM for a list of objects in the input text.
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are given a prompt from the user. You must take that prompt and "
                "answer back the list of objects that were written in the prompt. They must be separated by commas."
                "Your answer must be in the format: 'object1, object2, object3'. It must be in JSON format.",
            },
            {"role": "user", "content": f"{input_text}"},
        ],
        response_format={
            "type": "json_object",
            "schema": ImageDescription.model_json_schema(),
        }
    )
    output = json.loads(response.choices[0].message.content)
    return output["objects"]
    
    