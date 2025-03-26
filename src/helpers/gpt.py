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
    pass
