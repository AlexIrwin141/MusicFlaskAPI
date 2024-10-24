from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from flask_migrate import Migrate
import psycopg2
import os
# Import resources
from resources.artist import ArtistResource
from resources.album import AlbumResource
from resources.track import TrackResource
from resources.playlist import PlaylistResource
from resources.playlistTrack import playlistTrackResource
from resources.search_and_filter import TracksByArtist, SearchForArtist, PLaylistWithTrackName, ReverseTrackName

from models import db
import logging
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Music Flask API!", "status": "running"}) 

api.add_resource(ArtistResource, '/artist', '/artist/<int:artist_id>') # endpoint for artist queries
api.add_resource(AlbumResource, '/albums/<int:album_id>', '/artist/<int:artist_id>/albums', '/albums') # endpoint for album queries
api.add_resource(TrackResource, '/albums/<int:album_id>/tracks', '/tracks/<int:track_id>') #endpoint for track queries
api.add_resource(PlaylistResource, '/playlist/<int:playlist_id>', '/playlists') #endpoint for playlist queries
api.add_resource(playlistTrackResource, '/playlists/<int:playlist_id>/tracks/<int:track_id>')
api.add_resource(TracksByArtist, '/artist/<int:artist_id>/tracks') # endpoint for querying tracks by artist
api.add_resource(SearchForArtist, '/artists/search') # endpoint for querying artist by name or part of
api.add_resource(PLaylistWithTrackName, '/playlist/search/<int:track_id>') # endpoint for querying playlists containing a specified track
api.add_resource(ReverseTrackName, '/backtracks/<int:artist_id>') # trial endpoint just to see if I cound add a function in the query.
                                                                  #  This one to return track names in reverse order
# Errors not otherwise caught in the resources

# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Resource not found',
        'message': 'The requested resource could not be found.'
    }), 404

# Error handler for 400 Bad Request
@app.errorhandler(BadRequest)
def bad_request_error(error):
    return jsonify({
        'error': 'Bad request',
        'message': 'The request could not be understood or was missing required parameters.'
    }), 400

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Server error',
        'message': 'An internal server error occurred. Please try again later.'
    }), 500

# Generic error handler for unexpected exceptions
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.'
    }), 500


if __name__ == "__main__":
    #with app.app_context():
   #     db.create_all()
    app.run(debug=True)

