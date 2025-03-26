from openai import OpenAI


def gpt(prompt: str) -> str:
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt + '\nBe concise and clear.'}
        ]
    )
    res = completion.choices[0].message.content
    return res
