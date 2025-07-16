CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS
    programming_languages (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        summary text,
        text_embeddings vector (384)
    );

CREATE INDEX NONCONCURRENTLY ON programming_languages USING ybhnsw (text_embeddings vector_cosine_ops);