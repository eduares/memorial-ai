# ============================================================
# PARÂMETROS DE EXTRAÇÃO
# ============================================================
# Define os parâmetros que podem ser extraídos dos memoriais
# descritivos.
#
# Cada parâmetro possui:
# - um identificador utilizado internamente;
# - um nome de apresentação;
# - uma descrição da informação que deve ser localizada.

from retrieval import search_similar_documents
from llm import generate_answer

PARAMETERS = {
    "escopo_tecnico": {
        "label": "Escopo técnico",
        "descricao": "Identificar os serviços e atividades que fazem parte do objeto da contratação."
    },

    "local_execucao": {
        "label": "Local de execução",
        "descricao": "Identificar a unidade, cidade, estado ou endereço onde os serviços serão executados."
    },

    "prazo_contrato": {
        "label": "Prazo de contrato",
        "descricao": "Identificar a duração ou vigência prevista para o contrato."
    },

    "quantidade_profissionais": {
        "label": "Quantidade de profissionais",
        "descricao": "Identificar a quantidade total de profissionais prevista para execução do contrato."
    },

    "prazo_pagamento": {
        "label": "Prazo de pagamento",
        "descricao": "Identificar o prazo ou condição de pagamento estabelecido no documento."
    }
}

# ============================================================
# EXTRAÇÃO DE UM PARÂMETRO
# ============================================================
# Realiza a busca e extração de uma informação específica
# do memorial descritivo.
#
# O fluxo consiste em:
# 1. Buscar trechos relacionados ao parâmetro;
# 2. Combinar os resultados em um contexto;
# 3. Construir a pergunta para o modelo;
# 4. Enviar pergunta e contexto ao LLM;
# 5. Retornar a resposta gerada.

 # Realiza uma extração simplificada para testes.
def extract_parameter(parameter):

    # Recupera os trechos mais relevantes do documento
    # relacionados ao parâmetro informado.
    results = search_similar_documents(parameter)

    # Combina o conteúdo dos trechos recuperados em um único
    # contexto que será enviado ao modelo de linguagem.
    context = "\n\n".join(
        [result[0] for result in results]
    )

    # ========================================================
    # CONSTRUÇÃO DA PERGUNTA
    # ========================================================
    # Define a instrução que será enviada ao modelo de linguagem.
    #
    # Caso a informação não esteja disponível no contexto,
    # o modelo é orientado a informar que ela não foi encontrada.

    question = f"""
    Extraia do memorial a seguinte informação:

    {parameter}

    Caso não exista, responda:
    "Informação não encontrada."
    """
    # Envia a pergunta e o contexto recuperado ao modelo
    # de linguagem.
    answer = generate_answer(question, context)

    # Retorna a resposta produzida pelo modelo.
    return answer

# ============================================================
# EXECUÇÃO DIRETA
# ============================================================
# Permite executar o processo de extração diretamente pelo
# terminal, percorrendo todos os parâmetros definidos acima.

if __name__ == "__main__":

    # Percorre os parâmetros configurados.
    for parameter in PARAMETERS:
        print(f"\n===== {parameter} =====")

        # Executa a extração do parâmetro atual.
        result = extract_parameter(parameter)

        # Exibe o resultado obtido.
        print(result)