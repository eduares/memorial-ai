# ============================================================
# FRAGMENTAÇÃO DO TEXTO
# ============================================================
# Divide o conteúdo do documento em chunks menores para
# permitir o processamento posterior pelo mecanismo de RAG.
#
# O parâmetro overlap mantém uma parte do conteúdo anterior
# em cada novo chunk, ajudando a preservar o contexto entre
# os fragmentos.

def split_text(text, chunk_size=1200, overlap=200):

    # Armazena os chunks gerados durante o processamento.
    chunks = []

    # Define a posição inicial da leitura do texto.
    start = 0

    # Continua o processamento enquanto houver conteúdo
    # disponível no texto.

    while start < len(text):
        # Define o limite final do chunk atual.
        end = start + chunk_size

        # Extrai o trecho correspondente ao chunk.
        chunk = text[start:end]

        # Adiciona o chunk à lista de resultados.
        chunks.append(chunk)

        # Avança para o próximo trecho considerando a
        # sobreposição configurada.
        start += chunk_size - overlap
    # Retorna todos os chunks gerados.
    return chunks

# ============================================================
# TESTE DO MÓDULO
# ============================================================
# Permite testar a função diretamente quando o arquivo é
# executado como programa principal.

if __name__ == "__main__":

    # Cria um texto de exemplo para testar a fragmentação.
    texto = """
    Este é um memorial descritivo de exemplo para testar a divisão do texto
    em múltiplos chunks menores para processamento posterior.
    """ * 20

    # Executa a fragmentação utilizando os parâmetros padrão.
    resultado = split_text(texto)

    # Exibe a quantidade de chunks gerados.
    print(f"Quantidade de chunks: {len(resultado)}")

    # Exibe os primeiros caracteres de cada chunk para
    # facilitar a verificação do resultado durante o teste.
    for i, chunk in enumerate(resultado):
        print(f"\nChunk {i+1}")
        print(chunk[:200])