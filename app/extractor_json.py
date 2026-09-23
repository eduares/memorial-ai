# ============================================================
# EXTRAÇÃO ESTRUTURADA DE PARÂMETROS
# ============================================================
# Define os parâmetros avaliados no protótipo e coordena a recuperação
# de contexto e a interpretação pelo modelo de linguagem.
#
# A lógica diferencia os parâmetros que utilizam buscas específicas
# dos que utilizam busca semântica geral.
import json
import streamlit as st
from app.retrieval import search_similar_documents, search_scope_documents
from app.llm import generate_extraction


PARAMETERS = {
    "escopo_tecnico": {
        "label": "Escopo técnico",
        "descricao": "Localizar o objeto da contratação e os serviços técnicos que serão executados, especialmente as seções de objeto, escopo dos serviços e atividades previstas."
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

# Padroniza a resposta retornada pelo modelo para a interface.
def normalize_parameter_answer(parameter_name, answer):

    answer = answer.strip()

    # Informação não encontrada
    if (
        "não encontrado" in answer.lower()
        or "não encontrada" in answer.lower()
    ):
        return "Informação não encontrada."

    prefixes = {
        "escopo_tecnico": "Escopo técnico:",
        "local_execucao": "Local de execução:",
        "prazo_contrato": "Prazo de contrato:",
        "quantidade_profissionais": "Quantidade de profissionais:",
        "prazo_pagamento": "Prazo de pagamento:"
    }

    prefix = prefixes.get(parameter_name)

    if prefix and answer.lower().startswith(prefix.lower()):
        answer = answer[len(prefix):].strip()

    return answer

 # Recupera o contexto adequado e extrai um parâmetro específico.
def extract_parameter(parameter_name, parameter_config, arquivo):
    print("ENTROU NO EXTRACT_PARAMETER")

    st.write(f"🔎 Processando parâmetro: {parameter_config['label']}")

    label = parameter_config["label"]
    descricao = parameter_config["descricao"]


    # ============================================================
    # BUSCA
    # ============================================================

    if parameter_name == "escopo_tecnico":

        results = search_scope_documents(arquivo)

    elif parameter_name == "quantidade_profissionais":

        query = """
Quantidade de profissionais.
Número total de profissionais.
Quantidade de colaboradores.
Quantidade de pessoas.
Dimensionamento da equipe.
Composição da equipe.
Composição dos profissionais.
Equipe mínima.
Quadro de profissionais.
Função e quantidade.
Funções e respectivas quantidades.
Total de profissionais previstos para execução dos serviços.
"""

        results = search_similar_documents(
            query,
            arquivo,
            limit=8
        )

    elif parameter_name == "prazo_pagamento":

        query = """
Prazo de pagamento.
Condições de pagamento.
Condição de pagamento.
Pagamento da contratada.
Pagamento dos serviços.
Prazo para pagamento.
Prazo após medição.
Pagamento após medição.
Pagamento após aprovação da medição.
Faturamento.
Prazo para faturamento.
Nota fiscal e pagamento.
Vencimento.
Medição e pagamento.
Aprovação da medição e pagamento.
"""

        results = search_similar_documents(
            query,
            arquivo,
            limit=8
        )

    else:

        query = f"{label}. {descricao}"
        results = search_similar_documents(query, arquivo)

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

        if len(result) > 2:
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

    if parameter_name == "escopo_tecnico":

        prompt = f"""
Você é um extrator de informações de memoriais descritivos.

Sua tarefa é identificar o ESCOPO TÉCNICO da contratação.

Utilize EXCLUSIVAMENTE as informações presentes no CONTEXTO.

O escopo técnico deve apresentar:
- o objeto ou finalidade da contratação;
- os principais serviços e atividades previstos;
- as principais disciplinas, sistemas, áreas ou equipamentos envolvidos,
  quando estiverem presentes.

Não utilize conhecimento externo.
Não invente informações.
Não faça estimativas.
Não acrescente informações que não estejam no CONTEXTO.
Não copie a descrição do parâmetro como resposta.
Não explique sua resposta.

CONTEXTO:
{context}

Retorne somente o escopo técnico consolidado.

Se não houver informação suficiente, retorne exatamente:
Informação não encontrada.
"""

    elif parameter_name == "quantidade_profissionais":

        prompt = f"""
Você é um extrator de informações de memoriais descritivos.

Sua tarefa é identificar a QUANTIDADE DE PROFISSIONAIS prevista
para a execução dos serviços.

Utilize EXCLUSIVAMENTE as informações presentes no CONTEXTO.

REGRAS OBRIGATÓRIAS:

1. Se existir uma quantidade TOTAL explícita de profissionais,
   retorne essa quantidade.

2. Se não existir uma quantidade total explícita, mas existir uma
   composição de equipe com funções e respectivas quantidades,
   retorne as funções e suas quantidades.

3. NÃO some quantidades de funções diferentes.

4. NÃO calcule um total a partir das quantidades encontradas.

5. NÃO transforme quantidade de equipes em quantidade de profissionais.

6. NÃO utilize números de equipamentos, veículos, horas, valores,
   documentos, prazos ou outros números que não representem
   profissionais.

7. A informação deve estar explicitamente presente no CONTEXTO.

8. Não utilize conhecimento externo.

9. Não invente informações.

10. Não faça estimativas.

11. Não copie a descrição do parâmetro como resposta.

12. Não explique sua resposta.

CONTEXTO:
{context}

Retorne somente a informação encontrada sobre a quantidade de profissionais.

Se não houver informação suficiente, retorne exatamente:
Informação não encontrada.
"""

    elif parameter_name == "prazo_pagamento":

        prompt = f"""
Você é um extrator de informações de memoriais descritivos.

Sua tarefa é identificar o PRAZO OU CONDIÇÃO DE PAGAMENTO
estabelecido no documento.

Utilize EXCLUSIVAMENTE as informações presentes no CONTEXTO.

REGRAS OBRIGATÓRIAS:

1. Procure no CONTEXTO informações explicitamente relacionadas
   ao pagamento dos serviços ou da contratada.

2. Se houver um prazo de pagamento explícito, retorne o prazo.

3. Se houver uma condição de pagamento explicitamente relacionada
   ao prazo ou à forma de pagamento, retorne essa condição.

4. Informações sobre medição, faturamento, nota fiscal ou aprovação
   devem ser utilizadas somente quando estiverem explicitamente
   relacionadas ao pagamento.

5. NÃO transforme prazo de medição em prazo de pagamento.

6. NÃO transforme prazo de validação da medição em prazo de pagamento.

7. NÃO faça cálculos ou inferências para determinar o prazo.

8. NÃO utilize conhecimento externo.

9. NÃO invente informações.

10. NÃO estime ou complete informações ausentes.

11. NÃO copie a descrição do parâmetro como resposta.

12. NÃO explique sua resposta.

CONTEXTO:
{context}

Retorne somente a informação encontrada sobre o prazo ou condição
de pagamento.

Se não houver informação suficiente, retorne exatamente:
Informação não encontrada.
"""

    else:

        prompt = f"""
Você é um extrator de informações de memoriais descritivos.

Extraia somente a informação solicitada utilizando exclusivamente o CONTEXTO.

Não utilize conhecimento externo.
Não invente informações.
Não utilize informações presentes nas instruções como dados.
Não copie a descrição do parâmetro.
Não explique sua resposta.

PARÂMETRO:
{label}

CONTEXTO:
{context}

Retorne somente o valor encontrado.

Se a informação não estiver no contexto, retorne exatamente:
Informação não encontrada.
"""

    # ============================================================
    # GERA RESPOSTA COM O LLM
    # ============================================================


    answer = generate_extraction(
        prompt
    )

    answer = normalize_parameter_answer(
        parameter_name,
        answer
    )

    return answer

# Executa a extração para todos os parâmetros definidos.
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

    arquivo = "Empresa 7.docx"

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