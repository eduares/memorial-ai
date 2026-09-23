# ============================================================
# LLM
# ============================================================
# Responsável pela comunicação com o Ollama e pelo envio de prompts
# ao modelo de linguagem utilizado pelo protótipo.
import ollama

 # Envia uma pergunta e seu contexto ao modelo Llama 3 via Ollama
def generate_answer(question, context):

    prompt = f"""
    ...
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