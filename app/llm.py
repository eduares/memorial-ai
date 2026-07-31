import ollama

def generate_answer(question, context):
    prompt = f"""
Você é um especialista em análise de memoriais descritivos
para elaboração de propostas técnicas e comerciais.

Sua tarefa é localizar e extrair SOMENTE a informação solicitada.

INFORMAÇÃO SOLICITADA:
{question}

REGRAS:
- Responda apenas com a informação encontrada.
- Seja objetivo.
- Não invente informações.
- Caso a informação não exista claramente, responda:
"Informação não encontrada."

CONTEXTO:
{context}
"""

    response = ollama.chat(
        model = "llama3",
        messages=[
            {
                "role": "user",
                "content": prompt

            }
        ]
    )

    return response["message"]["content"]