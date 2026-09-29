# ============================================================
# CONFIGURAÇÕES DA APLICAÇÃO
# ============================================================
# Este módulo centraliza as principais configurações utilizadas
# pela aplicação, incluindo os diretórios de arquivos e os
# parâmetros de conexão com o banco de dados.

import os
from dotenv import load_dotenv

# ============================================================
# CARREGAMENTO DAS VARIÁVEIS DE AMBIENTE
# ============================================================
# Carrega as variáveis definidas no arquivo .env para que
# possam ser acessadas pela aplicação por meio de os.getenv().

load_dotenv()

# ============================================================
# DIRETÓRIOS DA APLICAÇÃO
# ============================================================
# Define os diretórios utilizados para armazenar os arquivos
# enviados pelo usuário e os arquivos processados durante
# a execução da aplicação.

UPLOAD_FOLDER = "data/uploads"
PROCESS_FOLDER = "data/processed"

# ============================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ============================================================
# Obtém as informações de conexão com o PostgreSQL a partir
# das variáveis de ambiente.
#
# As credenciais não são armazenadas diretamente no código,
# permitindo separar as configurações do ambiente do código
# da aplicação.

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")