def split_text(text, chunk_size=1200, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    texto = """
    Este é um memorial descritivo de exemplo para testar a divisão do texto
    em múltiplos chunks menores para processamento posterior.
    """ * 20

    resultado = split_text(texto)

    print(f"Quantidade de chunks: {len(resultado)}")

    for i, chunk in enumerate(resultado):
        print(f"\nChunk {i+1}")
        print(chunk[:200])