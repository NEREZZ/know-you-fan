from google import genai

client = genai.Client(api_key="")
def bot(pergunta):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{pergunta}",
    )

    return response.text
