# Memorial Inteligente

### Inteligência Artificial Aplicada à Automação do Processo Orçamentário

Protótipo desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) do MBA em Data Science & Analytics.

## Sobre o projeto

O Memorial Inteligente investiga a aplicação de Inteligência Artificial como ferramenta de apoio à interpretação de memoriais descritivos, permitindo recuperar informações relevantes e organizá-las em parâmetros de interesse para o processo de orçamentação.

A solução utiliza **Retrieval-Augmented Generation (RAG)**, combinando recuperação semântica de trechos dos documentos com um modelo de linguagem executado localmente.

## Objetivo

Desenvolver uma solução baseada em Inteligência Artificial capaz de extrair, interpretar e organizar informações presentes em memoriais descritivos, apoiando o processo de elaboração de orçamentos.

### Parâmetros avaliados

- Escopo técnico
- Local de execução
- Prazo de contrato
- Quantidade de profissionais
- Prazo de pagamento

## Evolução do projeto

O desenvolvimento foi realizado de forma iterativa. A **REV00** corresponde à primeira versão utilizada para estabelecer a linha de base. A **REV01** incorpora os ajustes realizados após a análise da primeira etapa e foi utilizada na segunda etapa de experimentação.

### REV00 — Etapa 1

A versão inicial contemplava carregamento de memoriais, extração de texto, fragmentação em chunks, geração de embeddings, armazenamento em PostgreSQL/pgvector, recuperação semântica, utilização do LLM para extração e interface em Streamlit.

### REV01 — Etapa 2

A versão utilizada na segunda etapa manteve a arquitetura geral e incorporou ajustes na extração de DOCX, reingestão, recuperação do escopo técnico, recuperação da quantidade de profissionais, recuperação do prazo de pagamento e regras de extração.

## Arquitetura

1. Upload do memorial descritivo;
2. Extração do conteúdo;
3. Fragmentação em chunks;
4. Geração dos embeddings;
5. Armazenamento dos vetores e metadados no PostgreSQL/pgvector;
6. Recuperação semântica ou estrutural dos trechos relevantes;
7. Envio do contexto ao modelo de linguagem;
8. Extração dos parâmetros ou resposta ao usuário;
9. Apresentação dos resultados na interface.

Os diagramas estão organizados em `docs/`.

## Tecnologias utilizadas

- Python
- Streamlit
- Dockker / Docker Compose
- PostgreSQL
- pgvector
- Ollama
- Llama 3
- Nomic Embed Text
- Visual Studio Code

## Estrutura do projeto

```text
app/
├── ui/
├── chatbot.py
├── chunking.py
├── config.py
├── database.py
├── embeddings.py
├── extractor.py
├── extractor_json.py
├── ingestion.py
├── llm.py
├── main.py
├── parser.py
├── rag.py
└── retrieval.py

data/
├── processed/
├── samples/
└── uploads/

docs/
├── arquitetura/
├── diagramas/
├── imagens/
└── resultados/
    ├── Etapa 1/
    ├── Etapa 2/
    └── Tabelas/

tests/
```

A pasta `data/samples/` contém os memoriais sintéticos utilizados na experimentação. `uploads/` e `processed/` são destinadas aos arquivos gerados durante a execução.

## Como executar

### Pré-requisitos

- Python 3.11 ou superior
- Ollama
- Docker / Docker Compose
- PostgreSQL com pgvector

### Instalação

```bash
git clone https://github.com/eduares/memorial-ai.git
python -m venv .venv
pip install -r requirements.txt
```

Configure as variáveis de ambiente conforme `.env.example` e execute:

```bash
streamlit run app/main.py
```

### Banco de dados

O PostgreSQL com extensão pgvector é executado por meio do Docker Compose, utilizando a imagem `pgvector/pgvector:pg16`.

Para iniciar o banco de dados:

```bash
docker compose up -d

## Resultados da experimentação

A solução foi avaliada em duas etapas utilizando 10 memoriais descritivos sintéticos e 5 parâmetros.

### Etapa 1 — REV00

- 50 avaliações
- 7 corretas
- 19 parciais
- 14 incorretas
- 10 não aplicáveis

Considerando os 40 casos aplicáveis, o percentual de classificações corretas foi de **17,50%**.

### Etapa 2 — REV01

- 50 avaliações
- 30 corretas
- 6 parciais
- 4 incorretas
- 10 não aplicáveis

Considerando os 40 casos aplicáveis, o percentual de classificações corretas foi de **75,00%**.

Os memoriais utilizados foram produzidos especificamente para a experimentação. Os detalhes das avaliações estão em `docs/resultados/`.

## Limitações

O protótipo ainda apresenta limitações na recuperação e interpretação de informações, especialmente quando os dados estão incompletos, distribuídos em diferentes partes do documento ou apresentam contextos semelhantes.

Os resultados foram obtidos com documentos sintéticos e não representam, por si só, validação em ambiente produtivo.

## Trabalhos futuros

- Aprimorar os mecanismos de recuperação e extração;
- Realizar testes em ambiente produtivo;
- Ampliar os parâmetros analisados;
- Realizar novos testes com diferentes tipos de documentos;
- Desenvolver uma saída organizada em tópicos ou blocos, contemplando informações gerais do material fornecido pelo cliente;
- Evoluir a solução para uma arquitetura baseada em agentes especializados;
- Desenvolver agentes para identificação de informações contratuais e apoio à composição de custos.

## Documentação

A pasta `docs/` reúne arquitetura, diagramas, imagens e resultados das etapas de experimentação.

As referências bibliográficas e a fundamentação acadêmica permanecem no TCC e não são duplicadas no repositório.

## Autor

**Eduardo Sousa Soares**  
MBA em Data Science & Analytics  
Trabalho de Conclusão de Curso — 2026
