from models import db, Track, Playlist
from flask import request
from flask_restful import Resource, reqparse, marshal_with, abort, fields



class playlistTrackResource(Resource):

    """
    Resource for managing the association between Playlists and Tracks.

    Methods:
        post(playlist_id, track_id): Add a track to a playlist.
        delete(playlist_id, track_id): Remove a track from a playlist.
    """

    def post(self, playlist_id, track_id):

        """
        Add a track to a specified playlist.

        Args:
            playlist_id (int): ID of the playlist.
            track_id (int): ID of the track to add to the playlist.

        Returns:
            Success message indicating the track was added.
        """

        # validate playlist and track
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            abort(404, message = f"Playlist with id {playlist_id} not found")
        track = Track.query.get(track_id)
        if not track:
            abort(404, message = f"Track with id {track_id} not found")

        # look and see if we already have this track in the playlist
        if track in playlist.tracks:
            return {"message": "This track is already in the playlist"}, 400

        #Add track to playliust
        playlist.tracks.append(track)
        db.session.commit()
        return {"message": "added track to playlist"}, 200
    
    def delete(self, playlist_id, track_id):


        """
        Remove a track from a specified playlist.

        Args:
            playlist_id (int): ID of the playlist.
            track_id (int): ID of the track to remove from the playlist.

        Returns:
            Success message indicating the track was removed.
        """

        # check it is a valid playlist

        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            abort(404, message = f"Playlist with id {playlist_id} not found")

        # check it is a valid track
        track = Track.query.get(track_id)
        if not track:
            abort(404, message = f"track with id {track_id} not found")

        #make sure the track is actually in the playlist
        if track not in playlist.tracks:
            abort(http_status_code=404, message="Track not found in playlist")

        #delete track from playlist
        playlist.tracks.remove(track)
        db.session.commit()

        return{"message": f"removed {track.title} from playlist {playlist.name}"}, 200


