# ============================================================
# RECUPERAÇÃO DE INFORMAÇÕES
# ============================================================
# Este módulo implementa os mecanismos de recuperação utilizados
# pelo RAG do Memorial Inteligente.
#
# São utilizadas duas estratégias principais:
#
# 1. Busca semântica:
#    Recupera os chunks mais semelhantes à pergunta utilizando
#    embeddings e distância vetorial.
#
# 2. Recuperação estrutural do escopo:
#    Reconstrói o documento e identifica seções relacionadas
#    ao objeto e ao escopo da contratação.
#
# Os resultados recuperados são posteriormente utilizados pelo
# modelo de linguagem para realizar a extração das informações.

from app.embeddings import generate_embedding
from app.database import get_connection

# ============================================================
# BUSCA SEMÂNTICA
# ============================================================
# Recupera os trechos do documento que apresentam maior
# similaridade semântica com a consulta realizada.
#
# O processo consiste em:
# 1. Gerar o embedding da consulta;
# 2. Consultar os vetores armazenados no PostgreSQL;
# 3. Restringir a busca ao documento selecionado;
# 4. Ordenar os resultados pela distância vetorial;
# 5. Retornar os chunks mais relevantes.

def search_similar_documents(query, arquivo, limit=8):

    # ========================================================
    # GERAÇÃO DO EMBEDDING DA CONSULTA
    # ========================================================
    # Converte a pergunta ou consulta do usuário em uma
    # representação vetorial utilizando o mesmo mecanismo
    # utilizado na geração dos embeddings dos documentos.

    embedding = generate_embedding(query)

    # ========================================================
    # CONEXÃO COM O BANCO
    # ========================================================
    # Abre uma conexão com o PostgreSQL para consultar os
    # documentos e seus respectivos embeddings.
    conn = get_connection()
    cursor = conn.cursor()

    # ========================================================
    # CONSULTA VETORIAL
    # ========================================================
    # Busca somente os chunks pertencentes ao arquivo que está
    # sendo analisado.
    #
    # A expressão:
    #
    # embedding <-> %s::vector
    #
    # calcula a distância entre o vetor armazenado no banco e
    # o embedding da consulta.
    #
    # Os resultados são ordenados pela menor distância, ou seja,
    # pelos trechos mais semelhantes à consulta.

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

    # ========================================================
    # EXECUÇÃO DA CONSULTA
    # ========================================================
    # Os parâmetros são enviados separadamente da consulta SQL:
    #
    # 1. embedding da pergunta;
    # 2. nome do arquivo;
    # 3. quantidade máxima de resultados.

    cursor.execute(
        sql,
        (embedding, arquivo, limit)
    )

     # Recupera os resultados retornados pelo PostgreSQL.

    results = cursor.fetchall()

    # Fecha os recursos utilizados na consulta.
    cursor.close()
    conn.close()

    # Retorna os chunks recuperados, seus metadados e
    # respectivas distâncias vetoriais.
    return results

# ============================================================
# RECUPERAÇÃO ESTRUTURAL DO ESCOPO
# ============================================================
# Esta função utiliza uma estratégia diferente da busca
# semântica.
#
# Em vez de procurar apenas os chunks mais semelhantes,
# reconstrói o conteúdo do documento e identifica seções
# relacionadas ao objeto e ao escopo da contratação.
#
# Essa abordagem foi utilizada para melhorar a recuperação
# das informações relacionadas ao escopo técnico.

def search_scope_documents(arquivo):
    """
    Reconstrói o documento e identifica seções relacionadas
    ao objeto e ao escopo da contratação.
    """

    # ========================================================
    # CONSULTA AO BANCO
    # ========================================================
    # Recupera todos os chunks pertencentes ao documento,
    # ordenados pela posição original de cada chunk.

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    SELECT
        content,
        metadata
    FROM documents
    WHERE metadata->>'arquivo' = %s
    ORDER BY (metadata->>'chunk')::int;
    """

    # Executa a consulta utilizando o nome do arquivo.

    cursor.execute(sql, (arquivo,))

    # Recupera todos os chunks encontrados.

    results = cursor.fetchall()

    # Fecha a conexão com o banco.
    cursor.close()
    conn.close()

    # Caso não existam registros para o documento,
    # retorna uma lista vazia.

    if not results:
        return []

    # ========================================================
    # RECONSTRUÇÃO DO DOCUMENTO
    # ========================================================
    # O primeiro chunk é utilizado integralmente.
    #
    # Para os chunks seguintes, os primeiros 200 caracteres
    # são desconsiderados para reduzir a repetição causada
    # pela sobreposição entre os chunks.

    full_text = results[0][0]

    for result in results[1:]:
        full_text += result[0][200:]

    # Divide o texto reconstruído em linhas para permitir
    # a identificação da estrutura do documento.

    lines = full_text.splitlines()

    # Importa o módulo utilizado para reconhecimento dos
    # padrões de títulos e seções.

    import re

    # ========================================================
    # PALAVRAS-CHAVE DE ESCOPO
    # ========================================================
    # Define termos que podem indicar uma seção relacionada
    # ao objeto ou escopo da contratação.

    scope_keywords = [
        "OBJETO",
        "OBJETO DA CONTRATAÇÃO",
        "OBJETIVO",
        "ESCOPO",
        "ESCOPO DOS SERVIÇOS",
        "DESCRIÇÃO DOS SERVIÇOS"
    ]

        # ========================================================
    # IDENTIFICAÇÃO DE TÍTULOS
    # ========================================================
    # Verifica se uma linha apresenta características de um
    # título ou cabeçalho de seção.
    #
    # São considerados exemplos como:
    #
    # 1. OBJETO
    # 4. OBJETO DA CONTRATAÇÃO
    # 5.1 SERVIÇOS MECÂNICOS
    # OBJETO
    # ESCOPO DOS SERVIÇOS

    def is_heading(line):

        # Remove espaços desnecessários.
        line = line.strip()

        # Expressão regular utilizada para reconhecer títulos
        # numerados ou escritos em letras maiúsculas.

        if not line:
            return False

        # Expressão regular utilizada para reconhecer títulos
        # numerados ou escritos em letras maiúsculas.

        pattern = (
            r"^(?:\d+(?:\.\d+)*[\.\)]?\s*)?"
            r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9]"
            r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9\s\-\/&(),]*$"
        )

        # Retorna True quando a linha corresponde ao padrão.

        return bool(re.match(pattern, line))

    # ========================================================
    # IDENTIFICAÇÃO DO NÍVEL DA SEÇÃO
    # ========================================================
    # Determina o nível hierárquico de um título numerado.
    #
    # Exemplos:
    #
    # 1       → nível 1
    # 1.1     → nível 2
    # 1.1.1   → nível 3

    def get_level(line):
        match = re.match(r"^(\d+(?:\.\d+)*)", line.strip())
        # Quando não existe numeração, considera nível 1.
        if not match:
            return 1
        # Conta a quantidade de níveis presentes na numeração.
        return len(match.group(1).split("."))


    # ========================================================
    # IDENTIFICAÇÃO DE SEÇÕES DE ESCOPO
    # ========================================================
    # Normaliza o título removendo sua numeração e verifica
    # se ele corresponde a alguma das palavras-chave definidas
    # anteriormente.

    def is_scope_section(line):
        normalized = re.sub(
            r"^\d+(?:\.\d+)*[\.\)]?\s*",
            "",
            line.strip()
        ).upper()

        # Verifica se o título corresponde exatamente a uma
        # palavra-chave ou se começa com uma delas.

        return any(
            keyword == normalized
            or normalized.startswith(keyword + " ")
            for keyword in scope_keywords
        )

    # ========================================================
    # IDENTIFICAÇÃO DAS SEÇÕES
    # ========================================================
    # Percorre todas as linhas do documento e captura o conteúdo
    # pertencente às seções relacionadas ao escopo.
    sections = []

    # Indica se uma seção de escopo está sendo capturada.

    capturing = False

    # Armazena temporariamente as linhas da seção atual.

    current_section = []

    # Armazena o nível hierárquico da seção atual.

    current_level = None

     # Percorre todas as linhas do documento reconstruído.

    for line in lines:

        # Remove espaços desnecessários.

        line = line.strip()

        # Ignora linhas vazias.

        if not line:
            continue

        # Verifica se a linha corresponde a um título.

        if is_heading(line):

            # Identifica o nível hierárquico do título.
            level = get_level(line)

            # =================================================
            # INÍCIO DE UMA SEÇÃO DE ESCOPO
            # =================================================
            # Quando o título corresponde a uma das palavras-
            # chave de escopo, inicia a captura da seção.

            if is_scope_section(line):

                # Caso já exista uma seção em construção,
                # armazena-a antes de iniciar a nova.

                if current_section:
                    sections.append(
                        "\n".join(current_section)
                    )

                # Inicia uma nova seção utilizando o título
                # identificado.

                current_section = [line]
                current_level = level
                capturing = True

                continue

            # =================================================
            # FIM DA SEÇÃO ATUAL
            # =================================================
            # Se outra seção do mesmo nível ou de nível superior
            # for encontrada, encerra a captura da seção atual.

            if capturing and level <= current_level:

                if current_section:
                    sections.append(
                        "\n".join(current_section)
                    )
                # Limpa o estado da seção atual.
                current_section = []
                current_level = None
                capturing = False

        # ====================================================
        # CAPTURA DO CONTEÚDO
        # ====================================================
        # Enquanto uma seção de escopo estiver ativa, adiciona
        # suas linhas ao conteúdo da seção atual.

        if capturing:
            current_section.append(line)

    # ========================================================
    # ARMAZENAMENTO DA ÚLTIMA SEÇÃO
    # ========================================================
    # Caso o documento termine enquanto uma seção ainda estiver
    # sendo capturada, adiciona essa seção ao resultado.

    if current_section:
        sections.append(
            "\n".join(current_section)
        )

    # Caso nenhuma seção relacionada ao escopo tenha sido
    # identificada, retorna uma lista vazia.

    if not sections:
        return []

    # ========================================================
    # CONSTRUÇÃO DO CONTEXTO
    # ========================================================
    # Combina todas as seções identificadas em um único contexto.

    context = "\n\n".join(sections)

    # Retorna o conteúdo recuperado juntamente com metadados
    # indicando que se trata de informações relacionadas ao
    # objeto e escopo da contratação.

    return [
        (
            context,
            {
                "arquivo": arquivo,
                "secao": "OBJETO E ESCOPO"
            }
        )
    ]

# ============================================================
# TESTE DIRETO DO MÓDULO
# ============================================================
# Permite testar a busca semântica diretamente pelo terminal
# quando este arquivo é executado como programa principal.

if __name__ == "__main__":

    # Define a pergunta utilizada no teste.
    pergunta = "Qual o prazo do contrato?"

    # Define o documento utilizado no teste.
    arquivo = "Empresa 4.docx"

    # Executa a busca semântica.
    resultados = search_similar_documents(
        pergunta,
        arquivo
    )

    # Exibe os resultados recuperados.
    for resultado in resultados:

        print("\nRESULTADO:")
        print(resultado[0])

        print("Metadata:")
        print(resultado[1])

        print("Distância:")
        print(resultado[2])