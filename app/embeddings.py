import ollama


def generate_embedding(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]


if __name__ == "__main__":
    texto = "Prazo contratual previsto em 12 meses."

    vetor = generate_embedding(texto)

    print(f"Tamanho do vetor: {len(vetor)}")
    print(vetor[:10])