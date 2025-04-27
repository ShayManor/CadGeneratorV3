import os
from base64 import b64encode

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')


def prompt_text(prompt: str, assistant: str = None, effort: str = None) -> str:
    client = OpenAI(api_key=API_KEY)
    if not assistant:
        completion = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            reasoning_effort=effort if effort else "low"
        )
        res = completion.choices[0].message.content
        return res
    else:
        assistant = client.beta.assistants.retrieve(
            assistant_id=assistant
        )
        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": prompt}]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            ai_response = messages.data[0].content[0].text.value
            return ai_response


def prompt_image(prompt: str, path: str) -> str:
    client = OpenAI()

    with open(path, "rb") as f:
        img_bytes = f.read()

    ext = os.path.splitext(path)[1].lower()
    if ext == ".png":
        mime = "image/png"
    elif ext in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    else:
        raise ValueError("Unsupported file extension for image")

    b64str = b64encode(img_bytes).decode("ascii")

    data_uri = f"data:{mime};base64,{b64str}"
    ask = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": data_uri}}
        ]
    }

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[ask]
    )
    res = completion.choices[0].message.content
    return res
