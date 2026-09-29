# ============================================================
# INGESTÃO DE DOCUMENTOS
# ============================================================
# Este módulo coordena o processo de ingestão dos memoriais
# descritivos na base utilizada pelo RAG.
#
# O fluxo realizado é:
# 1. Remoção de registros anteriores do mesmo documento;
# 2. Extração do texto;
# 3. Divisão do conteúdo em chunks;
# 4. Geração dos embeddings;
# 5. Armazenamento dos chunks, metadados e embeddings
#    no PostgreSQL.

import json

from app.parser import extract_text
from app.chunking import split_text
from app.embeddings import generate_embedding
from app.database import insert_document, get_connection

# ============================================================
# REMOÇÃO DE DOCUMENTO EXISTENTE
# ============================================================
# Remove da tabela documents todos os registros associados
# ao arquivo que será processado novamente.
#
# Essa etapa evita que uma nova ingestão do mesmo memorial
# gere registros duplicados na base vetorial.

def delete_existing_document(file_name):
    """
    Remove todos os registros existentes do documento
    antes de realizar uma nova ingestão.
    """
     # Abre uma conexão com o banco de dados.
    conn = get_connection()

    # Cria o cursor utilizado para executar o comando SQL.
    cursor = conn.cursor()

    try:

        # Define a consulta para localizar os registros
        # associados ao nome do arquivo.
        query = """
        DELETE FROM documents
        WHERE metadata->>'arquivo' = %s
        """
        # Executa a remoção utilizando o nome do arquivo
        # como parâmetro da consulta.
        cursor.execute(
            query,
            (file_name,)
        )

        # Armazena a quantidade de registros removidos.
        removed = cursor.rowcount

        # Confirma a transação no banco de dados.
        conn.commit()

        print(
            f"Registros antigos removidos: {removed}"
        )

    except Exception as e:

        # Em caso de erro, desfaz a transação realizada.
        conn.rollback()

        print(
            f"Erro ao remover registros antigos: {e}"
        )

        # Propaga o erro para que a aplicação possa tratá-lo
        # no nível superior.
        raise

    finally:

        # Fecha o cursor e a conexão independentemente de
        # a operação ter sido concluída com sucesso ou não.
        cursor.close()
        conn.close()

# ============================================================
# INGESTÃO DO DOCUMENTO
# ============================================================
# Executa o fluxo completo de processamento de um memorial
# descritivo antes de sua utilização pelo mecanismo de RAG.

def ingest_document(file_path, file_name):

    # ========================================================
    # 1. REMOVE VERSÃO ANTERIOR DO DOCUMENTO
    # ========================================================
    # Garante que registros antigos do mesmo arquivo sejam
    # removidos antes da nova ingestão.


    delete_existing_document(
        file_name
    )

    # ========================================================
    # 2. EXTRAÇÃO DO DOCUMENTO
    # ========================================================
    # Extrai o conteúdo textual do memorial a partir do
    # arquivo recebido.

    text = extract_text(
        file_path
    )


    # ========================================================
    # 3. DIVISÃO EM CHUNKS
    # ========================================================
    # Divide o texto extraído em fragmentos menores.
    #
    # Esses fragmentos serão utilizados individualmente na
    # geração dos embeddings e posteriormente na recuperação
    # semântica.

    chunks = split_text(
        text
    )

    print(
        f"Quantidade de chunks gerados: {len(chunks)}"
    )

    # ========================================================
    # 4. GERAÇÃO DE EMBEDDINGS + INSERÇÃO
    # ========================================================
    # Processa cada chunk individualmente.
    #
    # Para cada fragmento:
    # - são criados os metadados;
    # - é gerado o embedding;
    # - o conteúdo, os metadados e o vetor são armazenados
    #   no banco de dados.

    for i, chunk in enumerate(chunks):

        # Define os metadados associados ao chunk.
        # O número do chunk permite identificar sua posição
        # dentro do documento original.
        metadata = {
            "arquivo": file_name,
            "chunk": i + 1
        }

        # Gera a representação vetorial do conteúdo do chunk
        # utilizando o modelo de embeddings configurado.
        embedding = generate_embedding(
            chunk
        )

        # Armazena o conteúdo textual, os metadados e o
        # embedding na tabela utilizada pelo RAG.
        insert_document(
            chunk,
            json.dumps(metadata),
            embedding
        )

    # Informa que o processo de ingestão foi concluído.
    print(
        "Documento processado com sucesso!"
    )

# ============================================================
# TESTE DIRETO DO MÓDULO
# ============================================================
# Permite executar a ingestão de um documento diretamente
# quando este arquivo é executado como programa principal.

if __name__ == "__main__":

    # Define o caminho do memorial utilizado no teste.
    file_path = (
        "data/uploads/Empresa 4.docx"
    )

    # Define o nome do arquivo que será utilizado nos
    # metadados armazenados no banco.
    file_name = (
        "Empresa 4.docx"
    )

    # Executa o processo completo de ingestão.
    ingest_document(
        file_path,
        file_name
    )