from embeddings import generate_embedding
from database import get_connection

def search_similar_documents(query, limit=8):
    embedding = generate_embedding(query)

    conn = get_connection()
    cursor = conn.cursor()

    sql ="""
    SELECT content, metadata,
           embedding <-> %s::vector AS distance
    FROM documents
    ORDER BY distance
    LIMIT %s;
    """
    cursor.execute(sql,(embedding,limit))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

if __name__ == "__main__":
    pergunta = "Qual o prazo do contrato?"

    resultados = search_similar_documents(pergunta)

    for resultado in resultados:
        print("\nRESULTADO:")
        print(resultado[0])
        print("Distância:", resultado[2])  