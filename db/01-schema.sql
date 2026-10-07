-- TalkDesk schema. Shared by all three implementations.
--
-- Note what is missing: there is no index on talks.title. That is planted
-- defect D-2, and Week 3's load test is what finds it. Do not add one without
-- reading contract/CONTRACT.md first.

DROP TABLE IF EXISTS talks;
DROP TABLE IF EXISTS speakers;

CREATE TABLE speakers (
    id    SERIAL PRIMARY KEY,
    name  TEXT NOT NULL,
    email TEXT NOT NULL,
    bio   TEXT
);

CREATE TABLE talks (
    id         SERIAL PRIMARY KEY,
    speaker_id INTEGER NOT NULL REFERENCES speakers(id),
    title      TEXT NOT NULL,
    abstract   TEXT,
    track      TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'submitted',
    score      INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- speaker_id IS indexed: the N+1 (D-1) is about query *count*, not row scans.
-- Leaving this unindexed too would confuse the two lessons.
CREATE INDEX idx_talks_speaker ON talks(speaker_id);

-- Deliberately absent:
--   CREATE INDEX idx_talks_title ON talks(title);
