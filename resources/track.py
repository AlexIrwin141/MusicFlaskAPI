from models import db, Artist, Album, Track

from flask_restful import Resource, reqparse, marshal_with, abort, fields



track_args = reqparse.RequestParser()
track_args.add_argument('title', type = str, required = True, help = 'Track name is needed')
#track_args.add_argument('album_id', type = int, required = True, help = 'Album is needed')


trackFields = {
    'id':fields.Integer,
    'title':fields.String,
    'album_id':fields.Integer
    }


class TrackResource(Resource):

    """
    Resource for handling CRUD operations on Tracks.

    Methods:
        post(album_id): Create a new track associated with an album.
        get(album_id): Retrieve all tracks associated with an album.
        delete(track_id): Delete a specific track.
        put(track_id): Update a specific track's information.
    """

    @marshal_with(trackFields)
    def post(self, album_id):

        """
        Create a new track and associate it with a specified album.

        Args:
            album_id (int): ID of the album to associate the track with.

        Returns:
            List of all tracks in the album after the new track is added.
        """

        args = track_args.parse_args()
        # get album from the album id
        album = Album.query.get(album_id)
        if not album:
               abort(http_status_code=404, message="Album not found")
        
        new_track = Track(title = args["title"],
        album_id = album_id)

        db.session.add(new_track)
        db.session.commit()
        tracks = Track.query.filter_by(album_id = album_id).all()
        return tracks, 201
    



    
    @marshal_with(trackFields)
    def get(self, album_id):

        """
        Retrieve all tracks for a specified album.

        Args:
            album_id (int): ID of the album to retrieve tracks for.

        Returns:
            List of tracks for the specified album.
        """

        # get artist from the artist id
        album = Album.query.get(album_id)

        if not album:
                abort(http_status_code=404, message="Album not found")

        #this_album = Album.query.filter_by(id = album_id).first()
        
        album_tracks = Track.query.filter_by(album_id = album_id).all()
        if not album_tracks:
            abort(http_status_code=404, message="No tracks found for this albumb")
        return album_tracks, 200

    def delete(self, track_id):
    
        """
        Deletes trfack based on track ID.

        Args:
            track_id (int): ID of the specific track to remove.

        Returns:
            Name of track deleted.
        """

        track = Track.query.filter_by(id = track_id).first()
        if not track:
            abort(http_status_code=404, message="Track not found")
        db.session.delete(track)
        db.session.commit()
        return {'message': f'The track known as {track.title} has been deleted'}, 200
    
    @marshal_with(trackFields)
    def put(self, track_id):

        """
        Modifies track details on track ID.

        Args:
            track_id (int): ID of the specific track to modify.

        Returns:
            Details of newly modified track.
        """

        track = Track.query.get(track_id) 
        if not track:
             abort(404, message = 'Track not found')
        args = track_args.parse_args()
        track.title = args['title']

        if args['album_id']:
            album = args['album_id']
            new_album = Album.query.get(album)
            #new_name = args['name']
            if not new_album:
                abort(http_status_code=404, message="Album not found")
            track.album_id = album

        db.session.commit()
        return track, 200
        