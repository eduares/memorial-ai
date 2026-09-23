# ============================================================
# INGESTÃO
# ============================================================
# Executa o pipeline de entrada do documento: remoção de registros
# anteriores, extração, fragmentação em chunks, geração de embeddings
# e armazenamento no PostgreSQL/pgvector.
import json

from app.parser import extract_text
from app.chunking import split_text
from app.embeddings import generate_embedding
from app.database import insert_document, get_connection

# Evita duplicidade ao reprocessar um memorial com o mesmo nome.
def delete_existing_document(file_name):
    """
    Remove todos os registros existentes do documento
    antes de realizar uma nova ingestão.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
        DELETE FROM documents
        WHERE metadata->>'arquivo' = %s
        """

        cursor.execute(
            query,
            (file_name,)
        )

        removed = cursor.rowcount

        conn.commit()

        print(
            f"Registros antigos removidos: {removed}"
        )

    except Exception as e:

        conn.rollback()

        print(
            f"Erro ao remover registros antigos: {e}"
        )

        raise

    finally:

        cursor.close()
        conn.close()

 # Executa todas as etapas de preparação e armazenamento do documento.
def ingest_document(file_path, file_name):

    # ========================================================
    # 1. REMOVE VERSÃO ANTERIOR DO DOCUMENTO
    # ========================================================

    delete_existing_document(
        file_name
    )

    # ========================================================
    # 2. EXTRAÇÃO DO DOCUMENTO
    # ========================================================

    text = extract_text(
        file_path
    )

    # ========================================================
    # 3. DIVISÃO EM CHUNKS
    # ========================================================

    chunks = split_text(
        text
    )

    print(
        f"Quantidade de chunks gerados: {len(chunks)}"
    )

    # ========================================================
    # 4. GERAÇÃO DE EMBEDDINGS + INSERÇÃO
    # ========================================================

    for i, chunk in enumerate(chunks):

        metadata = {
            "arquivo": file_name,
            "chunk": i + 1
        }

        embedding = generate_embedding(
            chunk
        )

        insert_document(
            chunk,
            json.dumps(metadata),
            embedding
        )

    print(
        "Documento processado com sucesso!"
    )


if __name__ == "__main__":

    file_path = (
        "data/uploads/Empresa 4.docx"
    )

    file_name = (
        "Empresa 4.docx"
    )

    ingest_document(
        file_path,
        file_name
    )