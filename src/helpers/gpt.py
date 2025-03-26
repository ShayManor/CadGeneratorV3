from base64 import b64encode

from openai import OpenAI


def prompt_text(prompt: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="o3-mini",
        messages=[
            {"role": "user", "content": prompt + '\nBe concise and accurate.'}
        ]
    )
    res = completion.choices[0].message.content
    return res


def prompt_image(prompt: str, path: str) -> str:
    client = OpenAI()
    with open(path, 'rb') as f:
        contents = b64encode(f.read())
    ask = {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{contents}"
          }
        }
      ]
    }
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[ask]
    )
    res = completion.choices[0].message.content
    return res
