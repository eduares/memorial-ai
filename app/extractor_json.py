# ============================================================
# EXTRAÇÃO DOS PARÂMETROS
# ============================================================
# Este módulo coordena a extração estruturada das informações
# relevantes dos memoriais descritivos.
#
# O processo utiliza:
# - recuperação de trechos relevantes do documento;
# - construção de um contexto;
# - prompts específicos para cada parâmetro;
# - modelo de linguagem para interpretar o contexto;
# - normalização da resposta obtida.
#
# Os parâmetros analisados nesta versão são:
# - Escopo técnico;
# - Local de execução;
# - Prazo de contrato;
# - Quantidade de profissionais;
# - Prazo de pagamento.

import json
import streamlit as st
from app.retrieval import search_similar_documents, search_scope_documents
from app.llm import generate_extraction


# ============================================================
# PARÂMETROS ANALISADOS
# ============================================================
# Define os parâmetros que serão extraídos dos memoriais.
#
# Cada parâmetro possui:
# - um nome utilizado internamente pela aplicação;
# - um rótulo apresentado ao usuário;
# - uma descrição utilizada para orientar a recuperação
#   das informações.

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

# ============================================================
# NORMALIZAÇÃO DA RESPOSTA
# ============================================================
# Padroniza as respostas produzidas pelo modelo de linguagem.
#
# Essa etapa:
# - identifica quando o modelo não encontrou a informação;
# - remove os prefixos dos parâmetros quando eles aparecem
#   desnecessariamente na resposta;
# - mantém o conteúdo relevante retornado pelo modelo.

def normalize_parameter_answer(parameter_name, answer):

    # Remove espaços em branco no início e no final da resposta.
    answer = answer.strip()

    # --------------------------------------------------------
    # INFORMAÇÃO NÃO ENCONTRADA
    # --------------------------------------------------------
    # Verifica diferentes formas utilizadas pelo modelo para
    # indicar que a informação não foi encontrada.


    if (
        "não encontrado" in answer.lower()
        or "não encontrada" in answer.lower()
    ):
        return "Informação não encontrada."

    # Prefixos esperados para cada parâmetro.
    prefixes = {
        "escopo_tecnico": "Escopo técnico:",
        "local_execucao": "Local de execução:",
        "prazo_contrato": "Prazo de contrato:",
        "quantidade_profissionais": "Quantidade de profissionais:",
        "prazo_pagamento": "Prazo de pagamento:"
    }

    # Obtém o prefixo correspondente ao parâmetro analisado.
    prefix = prefixes.get(parameter_name)

    # Remove o prefixo caso o modelo tenha incluído essa
    # identificação no início da resposta.
    if prefix and answer.lower().startswith(prefix.lower()):
        answer = answer[len(prefix):].strip()

    return answer

# ============================================================
# EXTRAÇÃO DE UM PARÂMETRO
# ============================================================
# Executa o processo completo de extração de um parâmetro:
#
# 1. Identifica a estratégia de busca adequada;
# 2. Recupera os trechos relevantes;
# 3. Exibe informações de diagnóstico;
# 4. Constrói o contexto;
# 5. Seleciona o prompt específico;
# 6. Envia o prompt ao LLM;
# 7. Normaliza a resposta;
# 8. Retorna o resultado.

def extract_parameter(parameter_name, parameter_config, arquivo):
    print("ENTROU NO EXTRACT_PARAMETER")

    # Exibe na interface qual parâmetro está sendo processado.
    st.write(f"🔎 Processando parâmetro: {parameter_config['label']}")

    # Obtém o nome e a descrição do parâmetro
    label = parameter_config["label"]
    descricao = parameter_config["descricao"]


    # ========================================================
    # BUSCA DOS TRECHOS RELEVANTES
    # ========================================================
    # A estratégia de recuperação varia conforme o parâmetro.
    #
    # Alguns parâmetros possuem consultas específicas,
    # desenvolvidas durante a experimentação da REV01.

    if parameter_name == "escopo_tecnico":

        # Utiliza uma recuperação estrutural específica para
        # localizar seções relacionadas ao escopo do documento.
        results = search_scope_documents(arquivo)

    elif parameter_name == "quantidade_profissionais":

        # Consulta direcionada a diferentes formas de descrição
        # da quantidade e composição da equipe.
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

    # Consulta direcionada a termos relacionados a pagamento,
    # faturamento, medição e aprovação.
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

        # Para os demais parâmetros, a consulta é construída
        # utilizando o rótulo e a descrição do parâmetro.
        query = f"{label}. {descricao}"
        results = search_similar_documents(query, arquivo)

    # ========================================================
    # DIAGNÓSTICO DOS CHUNKS RECUPERADOS
    # ========================================================
    # Exibe informações dos resultados recuperados para auxiliar
    # na validação do mecanismo de busca durante os testes.
    #
    # São apresentados:
    # - conteúdo do chunk;
    # - metadados;
    # - distância, quando disponível.

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

        # Verifica se existe um terceiro elemento contendo
        # a distância calculada durante a recuperação.
        if len(result) > 2:
            print("\nDISTÂNCIA:")
            print(result[2])

    # ========================================================
    # CONSTRUÇÃO DO CONTEXTO
    # ========================================================
    # Combina os conteúdos recuperados em um único texto que
    # será encaminhado ao modelo de linguagem.

    if results:

        context = "\n\n".join(
            result[0]
            for result in results
        )


    else:

        # Define um contexto explícito quando nenhum trecho
        # relevante é recuperado.
        context = "Nenhuma informação relevante foi encontrada."


    # ========================================================
    # CONSTRUÇÃO DO PROMPT
    # ========================================================
    # Seleciona as instruções específicas de acordo com o
    # parâmetro que está sendo extraído.
    #
    # As regras abaixo são parte da lógica experimental da REV01
    # e orientam o LLM a utilizar somente o contexto recuperado.

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

        # Prompt genérico utilizado para os demais parâmetros.
        # A instrução orienta o modelo a retornar somente a
        # informação presente no contexto recuperado.

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

    # ========================================================
    # GERAÇÃO DA RESPOSTA PELO LLM
    # ========================================================
    # Envia o prompt construído ao modelo de linguagem por meio
    # da função generate_extraction(), responsável pela
    # comunicação com o Ollama.

    answer = generate_extraction(
        prompt
    )

    # ========================================================
    # NORMALIZAÇÃO DA RESPOSTA
    # ========================================================
    # Padroniza o resultado retornado pelo modelo antes de
    # disponibilizá-lo para as demais partes da aplicação.
    answer = normalize_parameter_answer(
        parameter_name,
        answer
    )

    return answer

# ============================================================
# EXTRAÇÃO DE TODOS OS PARÂMETROS
# ============================================================
# Executa a extração dos parâmetros definidos no dicionário
# PARAMETERS.
#
# Cada parâmetro é processado individualmente e o resultado
# é armazenado em um dicionário.

def extract_all_parameters(arquivo):

    results = {}

    # Percorre todos os parâmetros configurados.
    for parameter_name, parameter_config in PARAMETERS.items():

        # Executa a extração do parâmetro atual.
        result = extract_parameter(
            parameter_name,
            parameter_config,
            arquivo
        )

        # Armazena o resultado utilizando o nome interno
        # do parâmetro como chave.
        results[parameter_name] = result

    return results


# ============================================================
# TESTE DIRETO
# ============================================================
# Permite executar o processo completo de extração diretamente
# pelo terminal, sem depender da execução principal do Streamlit.

if __name__ == "__main__":

    # Define o memorial utilizado no teste direto.
    arquivo = "Empresa 7.docx"

    # Executa a extração de todos os parâmetros.
    resultado = extract_all_parameters(
        arquivo
    )

    print("\n")
    print("========================================")
    print("RESULTADO FINAL")
    print("========================================")

    # Exibe o resultado final em formato JSON.
    print(
        json.dumps(
            resultado,
            indent=4,
            ensure_ascii=False
        )
    )