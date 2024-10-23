from models import db, Artist, Album, Track, Playlist, playlist_tracks
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from flask import request, jsonify, make_response
from sqlalchemy import select, delete, or_

album_fields = {
                "id": fields.Integer,
                "name": fields.String
                }




artist_fields = {
                "id": fields.Integer,
                "name": fields.String,
                "albums": fields.List(fields.Nested(album_fields))
                }

track_fields = {
                "id": fields.Integer,
                "title": fields.String,
                "back_name": fields.String,
                "album": fields.Nested(album_fields)
                }


playlist_fields = {
                "id": fields.Integer,
                "name": fields.String,
                "tracks": fields.List(fields.Nested(track_fields))
                }

tracks_by_artist_fields = {
                            "artist_id": fields.Integer(attribute = "id"),
                            "artist_name": fields.String(attribute = "name"),
                            "tracks": fields.List(fields.Nested(track_fields))
                }


playlists_with_tracks_fields = {
                        "track_name": fields.String(attribute = 'title'),
                        "playlists": fields.List(fields.Nested(playlist_fields))
                        }

#                             "tracks": fields.List(fields.Nested(track_fields))



artist_search_args = reqparse.RequestParser()
artist_search_args.add_argument('name', type = str, required = True, help = 'Artist name or part of is needed')


def reverseString(thisStr):
    return thisStr[::-1]

# return all tracks by a specific artist
class TracksByArtist(Resource):

    """
    Resource for retrieving all tracks by a specific artist.

    Methods:
        get(artist_id): Retrieve tracks associated with a specific artist.
    """

    @marshal_with(track_fields)
    def get(self, artist_id):

        """
        Retrieve all tracks for a specified artist.

        Args:
            artist_id (int): ID of the artist to retrieve tracks for.

        Returns:
            List of tracks associated with the artist.
        """

        #make sure the artist is valid
        artist = Artist.query.get(artist_id)
        if not artist:
            abort(http_status_code=404, message="Artist not found")
        
        tracks = Track.query.join(Album).filter(Album.artist_id == artist_id).order_by(Album.name).all()

        return tracks

# search for artist based on artist name
class SearchForArtist(Resource):

    """
    Resource for searching artists by name.

    Methods:
        get(): Search for artists by name or part of the name.
    """

    @marshal_with(artist_fields)
    def get(self):

        """
        Search for artists by name or part of the name.

        Returns:
            List of artists matching the search criteria.
        """

        # get the name parameter from the query body
        args = artist_search_args.parse_args()
        name = args["name"]

        #look for anyartists containing the search string
        artists = Artist.query.filter(Artist.name.ilike(f'%{name}%')).all()

        return artists


# Search for playlists that have a particular track
class PLaylistWithTrackName(Resource):


    """
    Resource for retrieving all playlists containing a specific track.

    Methods:
        get(track_id): Retrieve playlists containing a specific track.
    """


    @marshal_with(playlist_fields)
#    @marshal_with(playlists_with_tracks_fields)
    def get(self, track_id):

        """
        Search for playlists containing a specific track.

        Returns:
            List of playlists matching the search criteria.
        """

        # Check to see that the track actually exists
        track = Track.query.get(track_id)
        if not track:
             abort(http_status_code=404, message="Track not found")            

        # Search for playlists containing this track
        playlists = Playlist.query.filter(Playlist.tracks.any(id = track_id)).all()
        #playlists = Playlist.query.join(Playlist.tracks).filter(Track.id == track_id).all()

        return  playlists

# just for fun reverse the track name. I know I could use a lambda function but I just
# want to see if I can call a function to modify data before returning it.
class ReverseTrackName(Resource):
    def get(self, artist_id):
        #make sure the artist is valid
        artist = Artist.query.get(artist_id)
        if not artist:
             abort(http_status_code=404, message="Artist not found")
        
        tracks = Track.query.join(Album).join(Artist).filter(Artist.id == artist_id).order_by(Album.name).all()
        result = []
        for track in tracks:
            backtrack = reverseString(track.title)
            result.append({
                    "track_id": track.id,
                    "track_name": backtrack,
                    "album_name": track.album.name
                    })
        reply = make_response(jsonify(result), 200)
        reply.headers["Content-Type"] = "application/json"

        return reply

        