CREATE ROLE new_user WITH LOGIN PASSWORD 'new_password'


SELECT rolname AS username
FROM pg_roles

GRANT ALL PRIVILEGES ON DATABASE music_db TO axthec

CREATE TABLE songs (
    song_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    release_year INT
);