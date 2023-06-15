-- на данном этапе лишь одна таблица, 
-- так как потенциальная таблица users не имеет смысла

-- время напоминания без часового пояса (UTC0), но это усмотрено в логике приложения 

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS notes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    owner_id BIGINT NOT NULL,
    note_title VARCHAR(100) NOT NULL,
    note_text TEXT,
    reminder_time TIMESTAMP,
    created_at TIMESTAMPTZ DEFAULT NOW()
);