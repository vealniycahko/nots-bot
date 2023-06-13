-- используется B-tree индекс, так как часто нужно выбирать из общей
-- таблицы заметок все заметки конкретного пользователя

CREATE INDEX IF NOT EXISTS notes_owners_id ON notes (owner_id);
