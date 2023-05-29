-- на данном этапе лишь одна таблица, 
-- так как потенциальная таблица users не имеет смысла

CREATE TABLE IF NOT EXISTS notes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    note_title VARCHAR(100) NOT NULL,
    note_text TEXT,
    reminder_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(owner_id, note_title)
);
