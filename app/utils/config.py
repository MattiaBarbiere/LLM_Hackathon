import torch

# Together.ai imports
from together import Together
from keys import TOGETHER_AI

MAX_CHAT_HISTORY = 10
VERBOSE = True
LOCAL_ASR = False
CUDA_AVAILABLE = torch.cuda.is_available()
USE_TOGETHER_AI = True
TELEGRAM_MAX_OUTPUT = 4096    # Telegram max output length

USER_MESSAGES = dict()    # dict of chat/group IDs and their messages
N_WORDS = dict()

llm_model = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
# auth defaults to os.environ.get("TOGETHER_API_KEY")
client = Together(
    api_key=TOGETHER_AI,
)
