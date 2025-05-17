from utils.config import *


def query_llm(input_text, user_id):

    if user_id not in N_WORDS:
        N_WORDS[user_id] = -1

    if N_WORDS[user_id] > 0:
        input_text += f" (in {N_WORDS[user_id]} words or less)"

    # add to message history
    if user_id in USER_MESSAGES:
        USER_MESSAGES[user_id].append({"role": "user", "content": input_text})
    else:
        USER_MESSAGES[user_id] = [{"role": "user", "content": input_text}]

    # prompt LLM
    response = client.chat.completions.create(
        model=llm_model,
        messages=USER_MESSAGES[user_id]
    )
    text_response = response.choices[0].message.content

    # update message history
    USER_MESSAGES[user_id].append({"role": "assistant", "content": text_response})

    if VERBOSE:
        print(USER_MESSAGES[user_id])

    # clear chat history (if too long)
    if len(USER_MESSAGES[user_id]) > 2 * MAX_CHAT_HISTORY:
        # remove bot response
        USER_MESSAGES[user_id].pop(0)
        # remove question
        USER_MESSAGES[user_id].pop(0)

    text_response = f"MODEL: {llm_model}\n\n{text_response}"
    # truncate response if too long
    if len(text_response) > TELEGRAM_MAX_OUTPUT:
        text_response = text_response[:TELEGRAM_MAX_OUTPUT-20] + "\n\nOUTPUT TRUNCATED"
    return text_response
