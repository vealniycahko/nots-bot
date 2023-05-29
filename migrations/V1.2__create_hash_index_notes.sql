-- несмотря на возможные повторения owner_id в notes, используется hash индекс,
-- так как нам часто нужно искать все записи с конкретным owner_id

CREATE INDEX IF NOT EXISTS notes_owner_id_hash ON notes USING hash (owner_id);
