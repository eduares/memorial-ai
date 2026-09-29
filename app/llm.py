import ollama


# Envia uma pergunta e seu contexto ao modelo Llama 3 via Ollama.
def generate_answer(question, context):

    prompt = f"""
Você é um assistente especializado na análise de memoriais descritivos.

Utilize exclusivamente as informações presentes no contexto recuperado
do documento para responder à pergunta do usuário.

Regras:
- Não invente informações.
- Não utilize informações externas ao contexto.
- Se a informação não estiver presente no contexto, informe que ela não foi encontrada.
- Responda de forma objetiva e clara.

CONTEXTO DO DOCUMENTO:
{context}

PERGUNTA DO USUÁRIO:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# Envia o prompt específico de extração ao modelo via Ollama.
def generate_extraction(prompt):

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]