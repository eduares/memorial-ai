# ============================================================
# GERAÇÃO DE EMBEDDINGS
# ============================================================
# Este módulo é responsável por transformar os textos dos
# documentos em representações vetoriais (embeddings).
#
# Os embeddings são gerados pelo modelo Nomic Embed Text,
# executado localmente por meio do Ollama.
#
# Os vetores gerados são utilizados posteriormente pelo
# mecanismo de recuperação semântica do RAG.

import ollama

# ============================================================
# GERAÇÃO DO EMBEDDING
# ============================================================
# Recebe um texto e gera sua representação vetorial utilizando
# o modelo Nomic Embed Text.

def generate_embedding(text):
    # Envia o texto ao modelo de embeddings por meio do Ollama.
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    # Retorna somente o vetor gerado pelo modelo.
    return response["embedding"]

# ============================================================
# TESTE DO MÓDULO
# ============================================================
# Permite testar a geração de embeddings diretamente quando
# este arquivo é executado como programa principal.

if __name__ == "__main__":

     # Define um texto de exemplo para geração do embedding.
    texto = "Prazo contratual previsto em 12 meses."

    # Gera o vetor correspondente ao texto de exemplo.
    vetor = generate_embedding(texto)

     # Exibe a quantidade de dimensões do vetor gerado.
    print(f"Tamanho do vetor: {len(vetor)}")

    #Exibe apenas os dez primeiros valores do vetor para
    # facilitar a verificação durante o teste.
    print(vetor[:10])