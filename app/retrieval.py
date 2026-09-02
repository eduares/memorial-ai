from embeddings import generate_embedding
from database import get_connection


def search_similar_documents(query, arquivo, limit=8):

    # Gera o embedding da pergunta
    embedding = generate_embedding(query)

    # Conecta ao PostgreSQL
    conn = get_connection()
    cursor = conn.cursor()

    # Busca somente os chunks do arquivo que está sendo analisado
    sql = """
    SELECT
        content,
        metadata,
        embedding <-> %s::vector AS distance
    FROM documents
    WHERE metadata->>'arquivo' = %s
    ORDER BY distance
    LIMIT %s;
    """

    # Ordem dos parâmetros:
    # 1. embedding
    # 2. nome do arquivo
    # 3. limite de resultados
    cursor.execute(
        sql,
        (embedding, arquivo, limit)
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


if __name__ == "__main__":

    pergunta = "Qual o prazo do contrato?"
    arquivo = "Empresa 1.docx"

    resultados = search_similar_documents(
        pergunta,
        arquivo
    )

    for resultado in resultados:

        print("\nRESULTADO:")
        print(resultado[0])

        print("Metadata:")
        print(resultado[1])

        print("Distância:")
        print(resultado[2])