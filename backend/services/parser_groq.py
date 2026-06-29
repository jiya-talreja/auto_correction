from pathlib import Path
from services.groq_client import client
path_prompt = Path("prompt/groq_prompt.txt")
model="llama-3.3-70b-versatile"
def parsor_json(text : str):
    with path_prompt.open("r",encoding="utf-8") as file:
        prompt=file.read()
    response=client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {
                "role":"system",
                "content":prompt
            },
            {
                "role":"user",
                "content":f"Raw text\n\n{text}"
            }
        ]
    )
    print("Response : " , response)
    print("ANSWER : ",response.choices[0].message.content)
    return response
