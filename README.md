# Memorial Inteligente

### Inteligência Artificial Aplicada à Automação do Processo Orçamentário

> Protótipo desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) do MBA em Data Science & Analytics.

---

> **⚠️ Status do Projeto**
>
> Este projeto está em desenvolvimento como parte de um Trabalho de Conclusão de Curso (TCC). Novas funcionalidades e melhorias serão adicionadas ao longo da pesquisa.
---

# Sobre o Projeto

A elaboração de orçamentos depende da análise de memoriais descritivos, documentos que apresentam informações técnicas, requisitos contratuais, escopo dos serviços e demais parâmetros necessários para a composição de um custo.

Esse processo normalmente é realizado de forma manual, exigindo que o profissional consulte documentos extensos para localizar informações relevantes, tornando a atividade suscetível a erros e demandando um elevado tempo de análise.

O Memorial AI foi desenvolvido com o objetivo de investigar a aplicação da Inteligência Artificial Generativa como ferramenta de apoio à interpretação desses documentos.

A solução utiliza a abordagem Retrieval-Augmented Generation (RAG), combinando modelos de linguagem de grande porte (LLMs) com busca vetorial, permitindo recuperar trechos semanticamente relevantes dos memoriais antes da geração das respostas.

O resultado é um sistema capaz de auxiliar profissionais na identificação das informações necessárias para elaboração de orçamentos técnicos.

---

# Objetivo Geral

Desenvolver uma solução baseada em Inteligência Artificial capaz de extrair, interpretar e organizar informações presentes em memoriais descritivos, apoiando o processo de elaboração de orçamentos.

---

# Objetivos Específicos

- Extrair automaticamente o conteúdo textual de memoriais descritivos;
- Processar e fragmentar os documentos em partes menores (chunks);
- Gerar embeddings utilizando modelos de linguagem;
- Armazenar os embeddings em banco vetorial PostgreSQL (pgvector);
- Recuperar informações relevantes utilizando Retrieval-Augmented Generation (RAG);
- Disponibilizar uma interface web para interação com os documentos;
- Identificar automaticamente parâmetros utilizados durante a elaboração de orçamentos.

---

# Arquitetura da Solução

O funcionamento do sistema ocorre em cinco etapas principais:

1. Upload do memorial descritivo;
2. Extração do conteúdo textual;
3. Geração dos embeddings;
4. Armazenamento em banco vetorial PostgreSQL;
5. Recuperação contextual via RAG para responder perguntas do usuário.

Um diagrama detalhado da arquitetura será disponibilizado na pasta `docs/arquitetura`.

---

# Tecnologias Utilizadas

- Python
- Streamlit
- PostgreSQL
- pgvector
- Docker
- Ollama
- Llama 3
- Nomic Embed Text
- Visual Studio Code

---

# Estrutura do Projeto

```text
app/
database/
data/
docker/
docs/
tests/
```

---

# Como Executar

## Opção 1 — Docker (recomendado)

Com essa opção, o Docker sobe o banco vetorial (**PostgreSQL + pgvector**) e a
aplicação **Streamlit**. O **Ollama roda nativamente no host** (fora do Docker)
para aproveitar a GPU da máquina — no macOS o Ollama em container roda apenas em
CPU, o que torna o processamento muito mais lento.

### Pré-requisitos

- Docker Desktop (com Docker Compose)
- [Ollama](https://ollama.com/download) instalado no host

### Passos

Clone o repositório:

```bash
git clone https://github.com/usuario/memorial-ai.git
cd memorial-ai
```

Inicie o Ollama no host e baixe os modelos (apenas na primeira vez):

```bash
ollama serve            # deixe rodando (usa a GPU do host)
ollama pull llama3
ollama pull nomic-embed-text
```

Suba os serviços com Docker:

```bash
docker compose up --build
```

O que acontece automaticamente:

1. `postgres` — sobe o PostgreSQL com a extensão **pgvector** e cria a tabela
   `documents` (scripts em `database/`);
2. `app` — sobe a aplicação Streamlit somente após o banco estar pronto. A
   aplicação se conecta ao Ollama do host via `host.docker.internal:11434`.

> A primeira execução do `ollama pull` é mais demorada porque os modelos (~5 GB)
> são baixados. Nas próximas vezes o download é reaproveitado.

Acesse a aplicação em:

```
http://localhost:8501
```

Para rodar em segundo plano:

```bash
docker compose up --build -d
```

Para parar os serviços:

```bash
docker compose down
```

Para parar e apagar todos os dados (banco e uploads):

```bash
docker compose down -v
```

## Opção 2 — Execução local (desenvolvimento)

### Pré-requisitos

- Python 3.11+
- PostgreSQL com pgvector
- Ollama

### Instalação

Clone o repositório:

```bash
git clone https://github.com/usuario/memorial-ai.git
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente (copie o exemplo):

```bash
cp .env.example .env
```

Execute a aplicação:

```bash
streamlit run app/main.py
```

---

# Resultados Atuais

Atualmente o sistema é capaz de:

- realizar upload de memoriais descritivos;
- extrair o conteúdo textual dos documentos;
- gerar embeddings;
- armazenar informações em banco vetorial;
- responder perguntas utilizando RAG;
- apresentar interface web para interação com os documentos.

Os testes iniciais foram realizados utilizando memoriais descritivos sintéticos desenvolvidos especificamente para validação do protótipo.

---

# Limitações

Embora o sistema já possua funcionalidades operacionais, a recuperação das informações ainda apresenta oportunidades de melhoria quanto à precisão das respostas.

Os experimentos atuais concentram-se na validação do método proposto utilizando documentos sintéticos, sendo prevista a realização de novos testes durante a evolução da pesquisa.

---

# Trabalhos Futuros

- Melhorar a precisão da recuperação vetorial;
- Automatizar completamente a identificação dos parâmetros orçamentários;
- Integrar o sistema ao preenchimento automático da planilha de preços;
- Avaliar o desempenho utilizando memoriais reais (quando autorizados);
- Comparar diferentes modelos de embeddings e LLMs.

---

# Autor

**Eduardo Sousa Soares**

MBA em Data Science & Analytics

Trabalho de Conclusão de Curso

2026