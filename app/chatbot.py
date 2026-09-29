from app.retrieval import search_similar_documents
from app.llm import generate_answer


# ============================================================
# CHATBOT
# ============================================================
# Executa perguntas feitas pelo usuário:
# 1. Recupera os trechos relevantes do memorial;
# 2. Monta o contexto;
# 3. Envia a pergunta e o contexto ao modelo de linguagem.


def ask_question(question, arquivo):

    # ========================================================
    # RECUPERAÇÃO DOS TRECHOS
    # ========================================================

    results = search_similar_documents(
        question,
        arquivo
    )

    # ========================================================
    # MONTA O CONTEXTO
    # ========================================================

    context = "\n\n".join(
        [result[0] for result in results]
    )

    print("\n===== CONTEXTO RECUPERADO =====")
    print(context)
    print("===== FIM DO CONTEXTO =====\n")

    # ========================================================
    # PROMPT DO CHAT
    # ========================================================

    prompt = f"""
Você é um assistente especializado em análise de
Memoriais Descritivos para apoio ao processo de orçamentação.

Responda à pergunta do usuário utilizando exclusivamente
as informações presentes no contexto recuperado do memorial.

Regras:
- Utilize somente informações presentes no contexto.
- Não invente informações.
- Não utilize conhecimento externo.
- Se a informação não estiver presente no contexto,
  informe que ela não foi encontrada.
- Responda de forma objetiva e clara.
- Não explique o processo de recuperação.

Contexto do memorial:
{context}

Pergunta do usuário:
{question}
"""

    # ========================================================
    # GERA RESPOSTA
    # ========================================================

    answer = generate_answer(
        prompt,
        context
    )

    print("\n===== RESPOSTA DO LLM =====")
    print(answer)
    print("===== FIM DA RESPOSTA =====\n")

    return answer