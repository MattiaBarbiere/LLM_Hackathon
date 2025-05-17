import torch

# Together.ai imports
from together import Together
from keys import TOGETHER_AI, HUGGING_FACE_KEY

MAX_CHAT_HISTORY = 10
VERBOSE = True
LOCAL_ASR = False
CUDA_AVAILABLE = torch.cuda.is_available()
USE_TOGETHER_AI = True
TELEGRAM_MAX_OUTPUT = 4096    # Telegram max output length

USER_MESSAGES = dict()    # dict of chat/group IDs and their messages
N_WORDS = dict()

llm_model = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
vision_model = "Qwen/Qwen2.5-VL-72B-Instruct"

# auth defaults to os.environ.get("TOGETHER_API_KEY")
client = Together(
    api_key=TOGETHER_AI,
)

# Hugging Face imports
API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_KEY}",
}
