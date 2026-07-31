import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def insert_document(content, metadata, embedding):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO documents (content, metadata, embedding)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (content, metadata, embedding))

        conn.commit()

        cursor.close()
        conn.close()

        print("Documento inserido com sucesso!")

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    conn = get_connection()
    print("Conexão OK")
    conn.close()