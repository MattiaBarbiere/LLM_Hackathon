import logging
import re

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

    # Normal text processing for QA
    text_response = query_llm(input_text, user_id)
    await update.message.reply_text(text_response)
