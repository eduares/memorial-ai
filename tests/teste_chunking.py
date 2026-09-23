# ============================================================
# TESTE DE CHUNKING
# ============================================================
# Script auxiliar para verificar a divisão do texto e identificar
# chunks que contenham marcações de tabelas.
from parser import extract_text
from chunking import split_text


arquivo = "data/uploads/Empresa 4.docx"


# ============================================================
# EXTRAI O DOCUMENTO
# ============================================================

texto = extract_text(arquivo)


# ============================================================
# GERA OS CHUNKS
# ============================================================

chunks = split_text(texto)


print("=" * 80)
print(f"TOTAL DE CHUNKS: {len(chunks)}")
print("=" * 80)


# ============================================================
# PROCURA TABELAS NOS CHUNKS
# ============================================================

for i, chunk in enumerate(chunks, start=1):

    if "[TABELA]" in chunk or "[FIM DA TABELA]" in chunk:

        print("\n")
        print("=" * 80)
        print(f"CHUNK {i} — CONTÉM TABELA")
        print("=" * 80)

        print(chunk)

        print("=" * 80)