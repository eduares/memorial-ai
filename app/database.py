# ============================================================
# BANCO DE DADOS
# ============================================================
# Este módulo é responsável pela comunicação com o PostgreSQL.
#
# As funções disponibilizadas permitem:
# - estabelecer uma conexão com o banco de dados;
# - inserir o conteúdo dos documentos;
# - armazenar os metadados;
# - armazenar os embeddings utilizados na recuperação
#   semântica dos documentos.


import psycopg2
from app.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

# ============================================================
# CONEXÃO COM O BANCO DE DADOS
# ============================================================
# Estabelece uma conexão com o PostgreSQL utilizando os
# parâmetros definidos nas variáveis de ambiente.

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# ============================================================
# INSERÇÃO DE DOCUMENTOS
# ============================================================
# Insere no banco de dados:
# - o conteúdo textual do chunk;
# - os metadados associados ao documento;
# - o embedding gerado para o conteúdo.
#
# Esses dados são posteriormente utilizados pelo mecanismo
# de recuperação semântica do RAG.

def insert_document(content, metadata, embedding):
    try:
        # Abre uma conexão com o banco de dados.
        conn = get_connection()
        # Cria um cursor para executar comandos SQL.
        cursor = conn.cursor()

        # Define o comando SQL responsável pela inserção
        # dos dados na tabela documents.
        query = """
        INSERT INTO documents (content, metadata, embedding)
        VALUES (%s, %s, %s)
        """

        # Executa a inserção utilizando os valores recebidos
        # pela função.
        cursor.execute(query, (content, metadata, embedding))

        # Confirma a transação para persistir os dados
        # no banco de dados.
        conn.commit()

        # Encerra o cursor e a conexão após a inserção.
        cursor.close()
        conn.close()

        print("Documento inserido com sucesso!")

    except Exception as e:

        # Exibe o erro ocorrido durante a operação de banco
        # de dados.
        print("Erro:", e)

# ============================================================
# TESTE DE CONEXÃO
# ============================================================
# Permite verificar diretamente se a aplicação consegue
# estabelecer uma conexão com o PostgreSQL quando este
# arquivo é executado como programa principal.
if __name__ == "__main__":
    # Tenta estabelecer a conexão com o banco.
    conn = get_connection()
    # Encerra a conexão após o teste.
    conn.close()