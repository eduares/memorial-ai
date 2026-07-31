from retrieval import search_similar_documents
from llm import generate_answer

def ask_question(question):
    results = search_similar_documents(question)
    context = "\n\n".join(
        [result[0] for result in results]
    )
    answer = generate_answer(question, context)

    return answer

if __name__ == "__main__":
    pergunta = input("Pergunta: ")

    resposta = ask_question(pergunta)

    print("\nResposta: \n")
    print(resposta)