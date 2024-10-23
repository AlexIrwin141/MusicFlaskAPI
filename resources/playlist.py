from models import db, Track, Playlist, playlist_tracks

from flask_restful import Resource, reqparse, marshal_with, abort, fields
from sqlalchemy import select, delete


playlist_args = reqparse.RequestParser()
playlist_args.add_argument('name', type = str, required = True, help = 'Playlist name is needed')


trackModifyFields = {
    'id':fields.Integer,
    'name':fields.String
}

trackFields = {
    'id':fields.Integer,
    'title':fields.String,
    'artist':fields.String(attribute=lambda track: track.album.artist.name)
}

playlistFields = {
    'id':fields.Integer,
    'name':fields.String,
    'tracks':fields.List(fields.Nested(trackFields))
    }


class PlaylistResource(Resource):

    """
    Resource for handling CRUD operations on Playlists.

    Methods:
        get(playlist_id): Retrieve all playlists or a specific playlist.
        post(): Create a new playlist.
        delete(playlist_id): Delete a specific playlist.
        put(playlist_id): Update a specific playlist's name.
    """

# Get playlist details
    @marshal_with(playlistFields)
    def get(self, playlist_id = None):
  
        """
        Retrieve playlist(s) based on playlist ID, or all playlists.

        Args:
            playlist_id (int, optional): ID of the specific playlist to retrieve.

        Returns:
            Playlist or list of playlists.
        """

        if not playlist_id:
            playlists = Playlist.query.all()
            if not playlists:
                abort(404, message = 'No playlists found')
            return playlists, 200

        else:
            playlist = Playlist.query.filter_by(id = playlist_id).first()
            if not playlist:
                abort(404, message = 'Playlist nopt found')
            return playlist, 200
    

# Add new playlist
    @marshal_with(playlistFields)
    def post(self):
        
        """
        Create a new playlist.

        Returns:
            List of all playlists after the new playlist is added.
        """

        args = playlist_args.parse_args()
        new_playlist = Playlist(name = args["name"])
        
        db.session.add(new_playlist)
        db.session.commit()
        return new_playlist, 201
    
# delete a playlist
    def delete(self, playlist_id):

        """
        Deletes playlist based on playlist ID.

        Args:
            playlist_id (int): ID of the specific playlist to remove.

        Returns:
            Name of playlist deleted.
        """

        playlist = Playlist.query.filter_by(id = playlist_id).first()
        if not playlist:
            abort(http_status_code=404, message="Playlist not found")

        # remove tracks from playlist in the playlist_tracks table
        db.session.execute(playlist_tracks.delete().where(playlist_tracks.c.playlist_id == playlist_id))
        db.session.delete(playlist)
        db.session.commit()
        return {'message': f'Removed playlist {playlist.name}'}, 200
        
# modify playlist
    @marshal_with(playlistFields)
    def put(self, playlist_id):


        """
        Modifies playlist details based on playlist ID.

        Args:
            playlist (int): ID of the specific playlist to modify.

        Returns:
            Details of newly modified playlist.
        """

        playlist = Playlist.query.get(playlist_id)
        if not playlist:
           abort(404, message = 'Playlist not found')
        args = playlist_args.parse_args()
        playlist.name = args['name']
        
        db.session.commit()
        return playlist, 200
        