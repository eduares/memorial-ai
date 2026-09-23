# ============================================================
# RETRIEVAL
# ============================================================
# Responsável pela recuperação de trechos do memorial armazenados
# no PostgreSQL/pgvector. A função de escopo utiliza uma abordagem
# estrutural para localizar seções relacionadas ao objeto e escopo.
from app.embeddings import generate_embedding
from app.database import get_connection

# Realiza busca vetorial restrita ao arquivo atualmente analisado.
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
# Recupera e reconstrói o conteúdo para localizar seções de objeto e escopo.
def search_scope_documents(arquivo):
    """
    Reconstrói o documento e identifica seções relacionadas
    ao objeto e ao escopo da contratação.
    """

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

    cursor.execute(sql, (arquivo,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    if not results:
        return []

    # Reconstrói o documento completo
    full_text = results[0][0]

    for result in results[1:]:
        full_text += result[0][200:]

    lines = full_text.splitlines()

    import re

    # Termos que podem indicar uma seção de escopo
    scope_keywords = [
        "OBJETO",
        "OBJETO DA CONTRATAÇÃO",
        "OBJETIVO",
        "ESCOPO",
        "ESCOPO DOS SERVIÇOS",
        "DESCRIÇÃO DOS SERVIÇOS"
    ]

    def is_heading(line):
        line = line.strip()

        if not line:
            return False

        # Exemplos:
        # 1. OBJETO
        # 4. OBJETO DA CONTRATAÇÃO
        # 5.1 SERVIÇOS MECÂNICOS
        # OBJETO
        # ESCOPO DOS SERVIÇOS

        pattern = (
            r"^(?:\d+(?:\.\d+)*[\.\)]?\s*)?"
            r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9]"
            r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9\s\-\/&(),]*$"
        )

        return bool(re.match(pattern, line))

    def get_level(line):
        match = re.match(r"^(\d+(?:\.\d+)*)", line.strip())

        if not match:
            return 1

        return len(match.group(1).split("."))

    def is_scope_section(line):
        normalized = re.sub(
            r"^\d+(?:\.\d+)*[\.\)]?\s*",
            "",
            line.strip()
        ).upper()

        return any(
            keyword == normalized
            or normalized.startswith(keyword + " ")
            for keyword in scope_keywords
        )

    sections = []

    capturing = False
    current_section = []
    current_level = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if is_heading(line):

            level = get_level(line)

            # Início de uma seção de escopo
            if is_scope_section(line):

                if current_section:
                    sections.append(
                        "\n".join(current_section)
                    )

                current_section = [line]
                current_level = level
                capturing = True

                continue

            # Encontrou outra seção do mesmo nível
            # ou de nível superior
            if capturing and level <= current_level:

                if current_section:
                    sections.append(
                        "\n".join(current_section)
                    )

                current_section = []
                current_level = None
                capturing = False

        if capturing:
            current_section.append(line)

    if current_section:
        sections.append(
            "\n".join(current_section)
        )

    if not sections:
        return []

    context = "\n\n".join(sections)

    return [
        (
            context,
            {
                "arquivo": arquivo,
                "secao": "OBJETO E ESCOPO"
            }
        )
    ]



if __name__ == "__main__":

    pergunta = "Qual o prazo do contrato?"
    arquivo = "Empresa 4.docx"

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