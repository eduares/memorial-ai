-- Índice vetorial para acelerar a busca por similaridade (distância L2 / <->).
CREATE INDEX IF NOT EXISTS documents_embedding_idx
    ON documents
    USING ivfflat (embedding vector_l2_ops)
    WITH (lists = 100);

-- Índice para filtrar rapidamente os chunks por arquivo (metadata->>'arquivo').
CREATE INDEX IF NOT EXISTS documents_metadata_idx
    ON documents
    USING gin (metadata);
