import os
from base64 import b64encode

import anthropic
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def prompt_text(prompt: str, system: str = None) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-7-sonnet-latest",
        system=system,
        max_tokens=10_000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    res = response.content[0].text
    return res


def prompt_image2(prompt: str, system: str, path: str) -> str:
    client = anthropic.Anthropic()
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
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime,
                            "data": b64str,
                        },
                    },
                    {
                        "type": "text",
                        "text": system
                    }
                ],
            }
        ],
    )
    print(message)
    return message.content[0].text


def prompt_image(prompt: str, system: str, path: str) -> str:
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
