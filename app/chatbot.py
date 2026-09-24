from retrieval import search_similar_documents
from llm import generate_answer

def ask_question(question, arquivo):
    results = search_similar_documents(question, arquivo)
    context = "\n\n".join(
        [result[0] for result in results]
    )
    answer = generate_answer(question, context)

    return answer

if __name__ == "__main__":
    arquivo = input("Arquivo: ")
    pergunta = input("Pergunta: ")

    resposta = ask_question(pergunta, arquivo)

    print("\nResposta: \n")
    print(resposta)