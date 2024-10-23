from models import db, Album, Artist
from flask import jsonify
import datetime

from flask_restful import Resource, reqparse, marshal_with, abort, fields


album_args = reqparse.RequestParser()
album_args.add_argument('name', type = str, required = True, help = 'Name of artist is needed')
#album_args.add_argument('release_date', type = lambda d: datetime.strptime(d, '%Y-%m-%d'), required = True, help = 'Release date is needed')
album_args.add_argument('release_date', type = str, required = True, help = 'Release date is needed')
album_args.add_argument('artist_id', type = int, help = 'Artist id is needed')


albumFields = {
    'id': fields.Integer,
    'name': fields.String,
    'release_date': fields.String,  # assuming this field needs to be formatted as a string
    'artist_id': fields.Integer,
    'artist_name': fields.String(attribute=lambda album: album.artist.name if album.artist else None)
}

class AlbumResource(Resource):

    """
    Resource for handling CRUD operations on Albums.

    Methods:
        post(artist_id): Create a new album for a specified artist.
        get(album_id, artist_id): Retrieve albums by album ID, artist ID, or all albums.
        delete(album_id): Delete an album by ID.
        put(album_id): Update an album by ID.
    """


    @marshal_with(albumFields)
    def post(self, artist_id):

        """
        Create a new album for a specified artist.

        Args:
            artist_id (int): ID of the artist to associate the album with.

        Returns:
            List of all albums by the artist after the new album is added.
        """

        args = album_args.parse_args()
        # get artist from the artist id
        artist = Artist.query.get(artist_id)
        if not artist:
            abort(http_status_code=404, message="Artist not found")
        try:
            rel_date = datetime.datetime.strptime(args['release_date'], "%Y-%m-%d")
        except ValueError:
            abort(http_status_code=400, message="Invalid date format. Use YYYY-mm-dd")
        
        # Create new album
        new_album = Album(name = args["name"],
        release_date = rel_date,
        artist_id = artist_id)
        
        db.session.add(new_album)
        db.session.commit()
        albums = Album.query.filter_by(artist_id = artist_id).order_by(Album.release_date).all()


        return albums, 201
    



    @marshal_with(albumFields)
    def get(self, album_id = None, artist_id = None):
          
        """
        Retrieve album(s) based on album ID, artist ID, or all albums.

        Args:
            album_id (int, optional): ID of the specific album to retrieve.
            artist_id (int, optional): ID of the artist to retrieve albums for.

        Returns:
            Album or list of albums with artist information.
        """       

        if artist_id is not None:
            # Get artist.
            this_artist = Artist.query.filter_by(id=artist_id).first()
            if not this_artist:
                abort(404, message="Artist not found")
        
            # Get albums by this artist
            artist_albums = this_artist.albums.order_by(Album.release_date).all()

            return artist_albums, 200



        elif album_id is not None:
         # Get album by id
            album = Album.query.filter_by(id=album_id).first()
            if not album:
                abort(404, message="Album not found")


            return album, 200



        else:
        # artist_id and album_id are both None: Return all albums regardless of artist
            all_albums = Album.query.order_by(Album.artist_id, Album.release_date).all()


        return all_albums, 200


    def delete(self, album_id):

        """
        Deletes album based on album ID.

        Args:
            album_id (int): ID of the specific album to remove.

        Returns:
            Name of album deleted.
        """

        album = Album.query.filter_by(id = album_id).first()
        if not album:
            abort(http_status_code=404, message="Album not found")
        db.session.delete(album)
        db.session.commit()
        return {'message': f'Album {album.name} was successfully deleted'}, 200
    
    @marshal_with(albumFields)
    def put(self, album_id):

        """
        Modifies album details based on album ID.

        Args:
            album_id (int): ID of the specific album to modify.

        Returns:
            Details of newly modified album.
        """

        album = Album.query.filter_by(id = album_id).first()
        if not album:
            abort(http_status_code=404, message="Album not found")

        args = album_args.parse_args()
        album.name = args['name']        

        # check artist and update
        artist = args['artist_id']
        new_artist = Artist.query.get(artist)
        if not new_artist:
            abort(http_status_code=404, message="Artist not found")
        album.artist_id = artist

        if args['release_date']:
            try:
                rel_date = datetime.datetime.strptime(args['release_date'], "%Y-%m-%d")
            except ValueError:
                abort(http_status_code=400, message="Invalid date format. Use YYYY-mm-dd instead.")
        album.release_date = rel_date

        db.session.commit()

        return album, 200
