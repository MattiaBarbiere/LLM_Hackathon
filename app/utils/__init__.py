# Together.ai imports
from together import Together
from keys import TOGETHER_AI, HUGGING_FACE_KEY

# auth defaults to os.environ.get("TOGETHER_API_KEY")
client = Together(
    api_key=TOGETHER_AI,
)

# Hugging Face imports
API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_KEY}",
}