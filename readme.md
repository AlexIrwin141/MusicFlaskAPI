Flask RESTful API for Music Library Management
This project is a Flask RESTful API that allows users to manage artists, albums, tracks, playlists, and associations between playlists and tracks. It also includes search and filter functionality for artists, tracks, and playlists.


Features
Create, retrieve, update, and delete (CRUD) operations for Artists, Albums, Tracks, and Playlists.
Many-to-many relationship between Tracks and Playlists.
Search functionality for finding artists and tracks.
Specialty features like reversing track names.

Features:
Manage artists, albums, and tracks
Organize tracks into playlists
Search tracks by artist and find playlists containing specific tracks
Fully RESTful API with proper HTTP methods and status codes
Error handling and validation

Technologies Used
Python with Flask (for the web framework)
PostgreSQL (for the database)
SQLAlchemy (for ORM and database interactions)
Flask-RESTful (for building REST APIs)

Setup Instructions:
Prerequisites
Python 3.x
PostgreSQL
pgAdmin for database management (optional)

Before running the application, make sure to set the necessary environment variables:  

# Set the FLASK_APP environment variable  
set FLASK_APP=main.py  

# Set the DATABASE_URL environment variable (replace with your actual database URL)
set DATABASE_URL=postgresql+psycopg2://<username>:<password>@localhost/<db_name>

Installation
Clone the Repository:
git clone https://github.com/AlexIrwin141/MusicFlaskAPI.git
cd MusicFlaskAPI

Set up Virtual Environment:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate


Set up PostgreSQL Database:
Create a PostgreSQL user and database. You can use pgAdmin for ease of use:
CREATE USER username WITH PASSWORD 'yourpassword';
CREATE DATABASE music_db OWNER username;

Run Database Migrations:
flask db init
flask db migrate
flask db upgrade

Run the Flask Application:
flask run



API Endpoints:

Artists
GET /artists – Retrieve all artists.  
GET /artists/<artist_id> – Retrieve a specific artist.  
POST /artists – Add a new artist.  
example body:  
   {  
    "name": "The Clash",  
    "nationality": "British",  
    "year_formed": 1976  
  }  
PUT /artists/<artist_id> – Update an existing artist.  
DELETE /artists/<artist_id> – Delete an artist.  

Albums  
GET /albums – Retrieve all albums.  
GET /albums/<album_id> – Retrieve a specific album.  
POST /artist/<int:artist_id>/albums – Add a new album for an artist.  
example body:  
{"name": "Combat Rock",  
"release_date": "1982-05-14"}   
PUT /albums/<album_id> – Update an album.  
DELETE /albums/<album_id> – Delete an album.  

Tracks  
GET /albums/<album_id>/tracks – Retrieve all tracks for an album.  
POST /albums/<album_id>/tracks – Add a new track to an album.  
example body:  
{"title": "Anarchy In The UK"}  
PUT /tracks/<track_id> – Update a track.  
DELETE /tracks/<track_id> – Delete a track.  

Playlists  
GET /playlists – Retrieve all playlists.  
GET /playlists/<playlist_id> – Retrieve a specific playlist.  
POST /playlists – Create a new playlist.  
example body:  
{"name": "A very punk playlist"}  
PUT /playlists/<playlist_id> – Update a playlist.  
DELETE /playlists/<playlist_id> – Delete a playlist.  

Playlist_Tracks  
POST /playlists/<int:playlist_id>/tracks/<int:track_id> - Add track to a playlist  
DELETE /playlists/<int:playlist_id>/tracks/<int:track_id> - Remove track from a playlist  
 
Search and Filter  
GET /artists/search – Search for artists by name (case insensitive).  
example body:  
{"name": "cl"}  
GET /artist/<int:artist_id>/tracks' – Retrieve all tracks by an artist.  
GET /playlist/search/<int:track_id> – Retrieve playlists containing a specific track.  
GET /backtracks/<int:artist_id> - Retrieve all tracks by an artist with the track name being reversed. I just wanted to see if I could use a function ewhen generating the response.  

Error Handling  
Each endpoint returns appropriate error messages in the following format when things go wrong:
{
  "message": "Artist not found"
}
404 Not Found: Resource doesn't exist
400 Bad Request: Invalid input
201 Created: Successful creation
200 OK: Successful retrieval or update
500 Internal Server Error: Unexpected issues


License
This project is licensed under the MIT License. See the LICENSE file for details.