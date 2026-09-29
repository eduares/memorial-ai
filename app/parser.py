# ============================================================
# EXTRAÇÃO DE CONTEÚDO DOS DOCUMENTOS
# ============================================================
# Este módulo é responsável por extrair o conteúdo textual
# dos documentos utilizados pelo Memorial Inteligente.
#
# São suportados atualmente:
# - arquivos PDF;
# - arquivos DOCX.
#
# No caso dos documentos DOCX, são considerados tanto os
# parágrafos quanto as informações presentes em tabelas.


import fitz
from docx import Document

# ============================================================
# EXTRAÇÃO DE ARQUIVOS PDF
# ============================================================
# Abre o arquivo PDF e percorre suas páginas para extrair
# o conteúdo textual disponível em cada uma delas.

def extract_pdf(file_path):

    # Abre o documento PDF utilizando a biblioteca PyMuPDF.
    document = fitz.open(file_path)

    # Lista que armazenará o texto extraído de cada página.
    text = []

     # Percorre todas as páginas do documento.
    for page in document:
        # Extrai o texto da página e adiciona à lista.
        text.append(page.get_text())

    # Fecha o documento após a extração.
    document.close()

    # Combina o conteúdo de todas as páginas em uma única
    # string, separando cada página por uma quebra de linha.
    return "\n".join(text)

# ============================================================
# EXTRAÇÃO DE ARQUIVOS DOCX
# ============================================================
# Extrai o conteúdo textual de documentos Word.
#
# Além dos parágrafos convencionais, a função percorre as
# tabelas existentes no documento para evitar a perda de
# informações estruturadas nesse formato.

def extract_docx(file_path):

    # Abre o documento DOCX.
    document = Document(file_path)

    # Lista que armazenará todo o conteúdo extraído.
    text = []

    # ========================================================
    # EXTRAÇÃO DOS PARÁGRAFOS
    # ========================================================
    # Percorre os parágrafos do documento e adiciona somente
    # aqueles que possuem conteúdo.

    for paragraph in document.paragraphs:

        # Remove espaços desnecessários e verifica se existe
        # conteúdo no parágrafo.
        if paragraph.text.strip():

            # Adiciona o texto do parágrafo à lista.
            text.append(paragraph.text.strip())

    # ========================================================
    # EXTRAÇÃO DAS TABELAS
    # ========================================================
    # Percorre as tabelas existentes no documento.
    #
    # Cada linha é transformada em uma sequência de valores
    # separados pelo caractere "|", preservando a estrutura
    # das informações apresentadas na tabela.

    for table in document.tables:

        # Percorre cada linha da tabela.
        for row in table.rows:

            # Armazena temporariamente os conteúdos das células
            # da linha atual.
            cells = []

            # Percorre todas as células da linha.
            for cell in row.cells:

                # Remove espaços desnecessários do conteúdo
                # da célula.
                cell_text = cell.text.strip()

                # Adiciona somente células que possuem conteúdo.
                if cell_text:
                    cells.append(cell_text)

            # Se a linha possuir conteúdo, combina as células
            # em uma única representação textual.
            if cells:
                text.append(" | ".join(cells))

    # Retorna todo o conteúdo extraído como uma única string.
    return "\n".join(text)

# ============================================================
# FUNÇÃO PRINCIPAL DE EXTRAÇÃO
# ============================================================
# Identifica o formato do arquivo e direciona o processamento
# para a função de extração correspondente.

def extract_text(file_path):

    # Verifica se o arquivo possui extensão PDF.
    if file_path.lower().endswith(".pdf"):
        return extract_pdf(file_path)

    # Verifica se o arquivo possui extensão DOCX.
    elif file_path.lower().endswith(".docx"):
        return extract_docx(file_path)

    # Caso o formato não seja suportado, interrompe o processo
    # informando o problema.
    else:
        raise ValueError("Formato de arquivo não suportado.")

# ============================================================
# TESTE DIRETO DO MÓDULO
# ============================================================
# Permite testar a extração de um documento diretamente
# quando este arquivo é executado como programa principal.

if __name__ == "__main__":
    # Define o documento utilizado no teste.
    caminho = "data/uploads/Empresa 4.docx"

    # Executa a função principal de extração.
    texto = extract_text(caminho)

    # Exibe no terminal o conteúdo extraído.
    print(texto)