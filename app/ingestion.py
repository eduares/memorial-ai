import json

from parser import extract_text
from chunking import split_text
from embeddings import generate_embedding
from database import insert_document


def ingest_document(file_path, file_name):
    text = extract_text(file_path)

    chunks = split_text(text)

    print(f"Quantidade de chunks gerados: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        metadata = {
            "arquivo": file_name,
            "chunk": i + 1
        }

        embedding = generate_embedding(chunk)

        insert_document(
            chunk,
            json.dumps(metadata),
            embedding
        )

    print("Documento processado com sucesso!")


if __name__ == "__main__":
    file_path = "data/uploads/MD eletromecânica - Teste 2.docx"
    file_name = "MD eletromecânica - Teste 2.docx"

    ingest_document(file_path, file_name)