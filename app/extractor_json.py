import json

from retrieval import search_similar_documents
from llm import generate_answer


PARAMETERS = {
    "escopo_tecnico": "Escopo técnico",
    "local_execucao": "Local de realização dos serviços",
    "data_visita_tecnica": "Data de visita técnica",
    "envio_proposta": "Envio da proposta",
    "prazo_contrato": "Prazo de contrato",
    "prazo_pagamento": "Prazo de pagamento",
    "prazo_medicao": "Prazo de medição",
    "multas": "Multas",
    "previsao_inicio": "Previsão de início",
    "modelo_remuneracao": "Modelo de remuneração do contrato",
    "quantidade_equipes": "Quantidade de equipes"
}


def extract_parameter(parameter_name):
    results = search_similar_documents(parameter_name)

    context = "\n\n".join(
        [result[0] for result in results]
    )

    prompt = f"""
    Extraia do memorial a seguinte informação:

    {parameter_name}

    Retorne SOMENTE a informação objetiva.

    Caso não exista, responda:
    "Informação não encontrada."
    """

    answer = generate_answer(prompt, context)

    return answer.strip()


def extract_all_parameters():
    extracted_data = {}

    for key, parameter in PARAMETERS.items():
        print(f"Extraindo: {parameter}")

        result = extract_parameter(parameter)

        extracted_data[key] = result

    return extracted_data


if __name__ == "__main__":
    resultado = extract_all_parameters()

    print("\nRESULTADO FINAL:\n")

    print(
        json.dumps(
            resultado,
            indent=4,
            ensure_ascii=False
        )
    )