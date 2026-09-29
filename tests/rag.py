# ============================================================
# RAG - TESTE DE EXTRAÇÃO E RESUMO
# ============================================================
# Script de teste da etapa de Retrieval-Augmented Generation (RAG).
# Monta um contexto a partir dos trechos recuperados e envia esse
# contexto ao modelo de linguagem para geração da resposta.

import json

from retrieval import search_similar_documents
from llm import generate_answer


# ============================================================
# CONFIGURAÇÃO
# ============================================================

ARQUIVO = "Empresa 4.docx"


# ============================================================
# PROMPT PARA EXTRAÇÃO ESTRUTURADA
# ============================================================

def build_prompt(context):
    prompt = f"""
Você é o Agente de Inteligência de Documentos, especializado na
análise de memoriais descritivos, termos de referência, escopos,
contratos, anexos técnicos e documentos de contratação utilizados
pela Engenharia de Vendas.

Sua função é transformar documentos não estruturados em informações
organizadas e úteis para orçamentação e elaboração de propostas.

Analise exclusivamente as informações presentes no contexto fornecido.

Não invente, estime ou presuma informações ausentes.

Quando uma informação não estiver disponível, informe:

"Não identificado no documento."

Quando houver divergência entre informações, apresente a divergência
e classifique como "A validar".

============================================================
CONTEXTO DO DOCUMENTO
============================================================

{context}

============================================================
TAREFA
============================================================

Extraia as informações relevantes do documento e produza DUAS
CAMADAS DE SAÍDA.

============================================================
CAMADA 1 — JSON ESTRUTURADO
============================================================

Retorne um JSON válido contendo:

{{
    "escopo_tecnico": "",
    "local_execucao": "",
    "prazo_contrato": "",
    "quantidade_profissionais": 0,
    "prazo_pagamento": ""
}}

Regras obrigatórias para preenchimento dos cinco parâmetros:

1. "escopo_tecnico"

Extraia as principais atividades e serviços que fazem parte do objeto
e do escopo da contratação.

Não inclua informações sobre equipe, treinamentos, responsabilidades
ou condições comerciais neste campo.

2. "local_execucao"

Identifique o local físico onde os serviços serão executados.

Quando houver nome da unidade e cidade/estado, apresente ambos.

Exemplo:
"Complexo Industrial Tecnoflex, Campinas – SP"

Não confunda local de execução com endereço da contratante.

3. "prazo_contrato"

Considere como prazo contratual informações apresentadas no documento
como:

- vigência;
- vigência prevista;
- prazo contratual;
- duração do contrato.

Não confunda prazo contratual com:

- prazo de pagamento;
- prazo de medição;
- prazo de resposta;
- prazo de entrega da proposta;
- prazo de mobilização.

Se o documento apresentar "Vigência prevista | 24 meses",
o valor correto é:

"24 meses"

4. "quantidade_profissionais"

Quando houver uma estrutura de equipe com função e quantidade,
some os quantitativos de TODAS as funções.

Não conte:

- número de funções;
- número de linhas da tabela;
- número de cargos distintos.

Exemplo:

Supervisor de Manutenção = 1
Eletricista = 3
Mecânico de Utilidades = 3
Mecânico Hidráulico = 1
Oficial Civil = 1
Auxiliar Civil = 1

Total correto = 10 profissionais.

Neste exemplo, o valor correto para "quantidade_profissionais" seria:

10

Não faça estimativas.

5. "prazo_pagamento"

Extraia somente informações que indiquem explicitamente o prazo
ou condição de pagamento à contratada.

Não confunda prazo de pagamento com:

- prazo contratual;
- vigência;
- prazo de medição;
- data de entrega da proposta;
- data de assinatura;
- data de mobilização;
- modelo de remuneração.

Se não existir uma informação explícita sobre prazo de pagamento,
retorne exatamente:

"Não identificado no documento."

IMPORTANTE:

"Preço global mensal" NÃO é prazo de pagamento.

"Preço global mensal" corresponde ao modelo/regime de remuneração
e não deve ser colocado em "prazo_pagamento".

Quando uma informação não estiver presente no contexto, utilize:

"Não identificado no documento."

Nunca deixe o campo vazio.

Regras:

- O JSON deve ser válido.
- Não inclua comentários dentro do JSON.
- Não invente informações.
- Utilize "Não identificado no documento." quando necessário.
- Não faça cálculos de custos.
- Não realize precificação.
- Não tome decisão GO/NO-GO.

============================================================
CAMADA 2 — RESUMO EXECUTIVO
============================================================

Após o JSON, apresente um resumo executivo estruturado
obrigatoriamente nos seguintes tópicos:

## 1. RESUMO DO DOCUMENTO

Apresente uma visão geral da contratação, incluindo contratante,
objeto, tipo de serviço, prazo, local e principais características.

## 2. ESCOPO E ATIVIDADES

Descreva as principais atividades e serviços previstos.

## 3. LOCAL E CONDIÇÕES DE EXECUÇÃO

Apresente local, unidade, regime de atendimento, mobilização,
horários e demais condições relevantes, quando disponíveis.

## 4. ORGANOGRAMA / COMPOSIÇÃO DA EQUIPE

Liste os profissionais previstos.

Utilize o formato:

| Função | Quantidade | Observações |
|---|---:|---|
| ... | ... | ... |

Não crie funções ou quantitativos não presentes no documento.

## 5. EQUIPAMENTOS, FERRAMENTAS E RECURSOS DE EXECUÇÃO

Apresente os recursos identificados, organizando quando possível em:

- Equipamentos
- Ferramentas
- EPIs e EPCs
- Veículos
- Materiais e insumos

Informe responsabilidades de fornecimento quando estiverem
explicitamente definidas.

## 6. RESPONSABILIDADES DA CONTRATADA

Liste as responsabilidades explicitamente atribuídas à contratada.

## 7. RESPONSABILIDADES DA CONTRATANTE

Liste as responsabilidades explicitamente atribuídas à contratante.

## 8. CONDIÇÕES CONTRATUAIS E COMERCIAIS

Apresente, quando disponíveis:

- prazo contratual;
- início previsto;
- modelo de remuneração;
- prazo de pagamento;
- prazo de medição;
- critérios de medição;
- multas;
- reajustes;
- garantias;
- datas relevantes;
- demais condições comerciais.

## 9. REQUISITOS TÉCNICOS, SEGURANÇA E CAPACITAÇÃO

Apresente:

- qualificações;
- experiência;
- treinamentos;
- normas de segurança;
- certificações;
- EPIs;
- EPCs;
- requisitos técnicos;
- requisitos de qualidade;
- documentação obrigatória.

## 10. LACUNAS, AMBIGUIDADES E INCONSISTÊNCIAS

Liste informações ausentes, incompletas, ambíguas ou divergentes
que possam dificultar a elaboração da proposta.

## 11. INFORMAÇÕES A VALIDAR

Liste objetivamente os pontos que precisam ser confirmados antes
da elaboração da proposta.

============================================================
REGRAS FINAIS
============================================================

Utilize exclusivamente as informações presentes no contexto.

Não invente informações.

Não estime valores.

Não faça precificação.

Não realize cálculos de custos.

Não tome decisão GO/NO-GO.

Mantenha linguagem objetiva e adequada à Engenharia de Vendas.

Evite repetir integralmente o memorial.

O objetivo é transformar o documento em informação estruturada
e em uma visão executiva útil para análise e elaboração da proposta.

============================================================
REGRAS DE CONSISTÊNCIA
============================================================

Antes de gerar o resumo executivo, verifique se as informações
extraídas são coerentes com o contexto fornecido.

O resumo executivo deve utilizar prioritariamente as informações
efetivamente encontradas no contexto.

Quando uma informação estiver presente no JSON estruturado,
ela não deve ser apresentada como "Não identificado no documento"
no resumo.

Não altere, contradiga ou substitua informações já identificadas
na CAMADA 1.

Quando houver uma informação numérica relacionada à equipe,
confira novamente a soma dos quantitativos antes de gerar a resposta.

Quando houver informações de datas, diferencie:

- entrega da proposta;
- assinatura contratual;
- mobilização;
- início previsto;
- vigência contratual.

Não trate essas informações como equivalentes.

Quando houver "Preço global mensal", classifique como
"Modelo de remuneração" e nunca como "Prazo de pagamento".

Não crie informações para preencher campos ausentes.

"""

    return prompt


# ============================================================
# MONTA O CONTEXTO DO RAG
# ============================================================

def build_context(results):
    context_parts = []

    for i, result in enumerate(results, start=1):

        content = result[0]
        metadata = result[1]

        context_parts.append(
            f"""
[TRECHO {i}]
Fonte: {metadata.get('arquivo', 'Não informado')}
Chunk: {metadata.get('chunk', 'Não informado')}

{content}
"""
        )

    return "\n".join(context_parts)


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("TESTE DE EXTRAÇÃO ESTRUTURADA + RESUMO EXECUTIVO")
    print("=" * 60)

    print(f"\nArquivo: {ARQUIVO}")
    print("\nProcessando...")

    # --------------------------------------------------------
    # 1. BUSCA DOS CHUNKS
    # --------------------------------------------------------

    pergunta = """
    Extraia as principais informações necessárias para análise,
    dimensionamento e elaboração de uma proposta comercial,
    incluindo escopo, equipe, recursos, condições contratuais,
    responsabilidades, requisitos técnicos e informações ausentes.
    """

    resultados = search_similar_documents(
        pergunta,
        ARQUIVO,
        limit=8
    )

    # --------------------------------------------------------
    # 2. MONTA CONTEXTO
    # --------------------------------------------------------

    context = build_context(resultados)

    # --------------------------------------------------------
    # 3. MONTA PROMPT
    # --------------------------------------------------------

    prompt = build_prompt(context)

    # --------------------------------------------------------
    # 4. ENVIA AO LLM
    # --------------------------------------------------------

    resposta = generate_response(prompt)

    # --------------------------------------------------------
    # 5. EXIBE RESULTADO
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("RESPOSTA DO MEMORIAL INTELIGENTE")
    print("=" * 60)

    print(resposta)

    print("\n")
    print("=" * 60)
    print("FIM DO TESTE")
    print("=" * 60)