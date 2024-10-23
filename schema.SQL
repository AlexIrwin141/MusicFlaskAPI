CREATE TABLE artist (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(70) NOT NULL, 
	nationality VARCHAR(70) NOT NULL, 
	year_formed INTEGER
);
CREATE TABLE playlist (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(70) NOT NULL
);
CREATE TABLE album (
	id SERIAL PRIMARY KEY, 
	name VARCHAR(75) NOT NULL, 
	release_date TIMESTAMP, 
	artist_id INT NOT NULL, 
	FOREIGN KEY (artist_id) REFERENCES artist(id) ON DELETE CASCADE);

CREATE TABLE track (
	id SERIAL PRIMARY KEY, 
	title VARCHAR(75) NOT NULL, 
	album_id INTEGER NOT NULL
	FOREIGN KEY (album_id) REFERENCES album(id) ON DELETE CASCADE)
);
CREATE TABLE playlist_tracks (
	playlist_id INTEGER NOT NULL, 
	track_id INTEGER NOT NULL, 
	PRIMARY KEY (playlist_id, track_id), 
	FOREIGN KEY(playlist_id) REFERENCES playlist (id), 
	FOREIGN KEY(track_id) REFERENCES track (id)
);
