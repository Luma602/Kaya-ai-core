
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def online_ai(prompt):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are Kaya, a helpful public AI assistant."},
            {"role":"user","content":prompt}
        ]
    )
    return r.choices[0].message.content
