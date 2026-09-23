# ============================================================
# EXTRACTOR - VERSÃO DE TESTE
# ============================================================
# Implementação simplificada utilizada para testes de extração.
# A versão integrada da aplicação está em extractor_json.py.

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

 # Realiza uma extração simplificada para testes.
def extract_parameter(parameter):
    results = search_similar_documents(parameter)

    context = "\n\n".join(
        [result[0] for result in results]
    )

    question = f"""
    Extraia do memorial a seguinte informação:

    {parameter}

    Caso não exista, responda:
    "Informação não encontrada."
    """

    answer = generate_answer(question, context)

    return answer


if __name__ == "__main__":
    for parameter in PARAMETERS:
        print(f"\n===== {parameter} =====")

        result = extract_parameter(parameter)

        print(result)