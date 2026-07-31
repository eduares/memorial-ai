from retrieval import search_similar_documents
from llm import generate_answer


PARAMETERS = [
    "Escopo técnico",
    "Local de realização dos serviços",
    "Data de visita técnica",
    "Envio da proposta",
    "Prazo de contrato",
    "Prazo de pagamento",
    "Prazo de medição",
    "Multas",
    "Previsão de início",
    "Modelo de remuneração do contrato",
    "Quantidade de equipes"
]


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