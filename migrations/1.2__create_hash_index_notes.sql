-- используется GIN индекс, так как часто нужно выбирать из общей
-- таблицы заметок все заметки конкретного пользователя

-- CREATE INDEX IF NOT EXISTS notes_owners_id_gin ON notes USING GIN (owner_id gin__int8_ops);
