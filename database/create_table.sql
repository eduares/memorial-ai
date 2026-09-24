-- Tabela de armazenamento dos chunks dos memoriais e seus embeddings.
-- A dimensão 768 corresponde ao modelo de embeddings "nomic-embed-text".
CREATE TABLE IF NOT EXISTS documents (
    id        BIGSERIAL PRIMARY KEY,
    content   TEXT        NOT NULL,
    metadata  JSONB       NOT NULL DEFAULT '{}'::jsonb,
    embedding VECTOR(768) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
