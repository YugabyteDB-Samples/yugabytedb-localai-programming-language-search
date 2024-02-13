CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS
    programming_languages (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        summary text,
        text_embeddings vector (384)
    );