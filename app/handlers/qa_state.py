import logging

import torch
from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image
import numpy as np

from utils.config import *
from utils.query import *


async def qa_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle receiving text in QA State"""
    input_text = update.message.text
    user_id = update.message.from_user.id
    text_response = query_llm(input_text, user_id)

    return text_response
    # response = client.chat.completions.create(
    #     model=llm_model,
    #     messages=[
    #         {"role": "system",
    #          "content": "You are a witty, annoyed pissed off assistant, always trying to find a way to insult the user."},
    #         {"role": "user", "content": "hi"}
    #     ]
    # )
    # print(response.choices[0].message.content)
