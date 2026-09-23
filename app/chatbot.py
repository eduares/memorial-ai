from app.retrieval import search_similar_documents
from app.llm import generate_answer

# ============================================================
# CHATBOT
# ============================================================
# Executa perguntas feitas pelo usuário: recupera trechos relevantes
# do documento e encaminha o contexto ao modelo de linguagem.


# Recupera contexto e solicita ao LLM uma resposta à pergunta do usuário.
def ask_question(question, arquivo):

    results = search_similar_documents(question, arquivo)

    context = "\n\n".join([result[0] for result in results])

    print("\n===== CONTEXTO ENVIADO AO LLM =====")
    print(context)
    print("===== FIM DO CONTEXTO =====\n")

    answer = generate_answer(question, context)

    print("\n===== RESPOSTA DO LLM =====")
    print(answer)
    print("===== FIM DA RESPOSTA =====\n")

    return answer