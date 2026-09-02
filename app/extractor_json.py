import json
import streamlit as st
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


def extract_parameter(parameter_name, parameter_config, arquivo):
    print("ENTROU NO EXTRACT_PARAMETER")

    st.write(f"🔎 Processando parâmetro: {parameter_config['label']}")

    label = parameter_config["label"]
    descricao = parameter_config["descricao"]

    # ============================================================
    # BUSCA SEMÂNTICA
    # ============================================================

    query = f"{label}. {descricao}"

    results = search_similar_documents(
        query,
        arquivo
    )

    # ============================================================
    # DIAGNÓSTICO DOS CHUNKS RECUPERADOS
    # ============================================================

    print("\n========================================")
    print(f"PARÂMETRO: {label}")
    print(f"ARQUIVO: {arquivo}")
    print(f"QUANTIDADE DE RESULTADOS: {len(results)}")
    print("========================================")

    for i, result in enumerate(results, start=1):

        print(f"\n--- CHUNK {i} ---")

        print("\nCONTEÚDO:")
        print(result[0])

        print("\nMETADATA:")
        print(result[1])

        print("\nDISTÂNCIA:")
        print(result[2])
    # ============================================================
    # MONTA O CONTEXTO PARA O LLM
    # ============================================================

    if results:

        context = "\n\n".join(
            result[0]
            for result in results
        )

    else:

        context = "Nenhuma informação relevante foi encontrada."


    # ============================================================
    # PROMPT
    # ============================================================

    prompt = f"""
Você é um especialista em análise de Memoriais Descritivos
para processos de orçamentação.

Analise exclusivamente as informações presentes no contexto
fornecido.

Parâmetro:
{label}

Descrição:
{descricao}

Regras:

- Utilize somente informações presentes no contexto.
- Não invente informações.
- Não utilize conhecimento externo.
- Caso a informação não esteja presente no contexto,
  responda exatamente:

"Informação não encontrada."

- Retorne somente a informação correspondente ao parâmetro.
- Não explique o processo de análise.
- Não repita as instruções.
- Não diga "a resposta é".
- Seja objetivo.

Contexto do Memorial Descritivo:

{context}
"""

    # ============================================================
    # GERA RESPOSTA COM O LLM
    # ============================================================

    answer = generate_answer(
        prompt,
        context
    )

    return answer.strip()


def extract_all_parameters(arquivo):

    results = {}

    for parameter_name, parameter_config in PARAMETERS.items():

        result = extract_parameter(
            parameter_name,
            parameter_config,
            arquivo
        )

        results[parameter_name] = result

    return results


# ============================================================
# TESTE DIRETO
# ============================================================

if __name__ == "__main__":

    arquivo = "Empresa 1.docx"

    resultado = extract_all_parameters(
        arquivo
    )

    print("\n")
    print("========================================")
    print("RESULTADO FINAL")
    print("========================================")

    print(
        json.dumps(
            resultado,
            indent=4,
            ensure_ascii=False
        )
    )