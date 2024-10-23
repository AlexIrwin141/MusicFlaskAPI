from models import db, Artist


from flask_restful import Resource, reqparse, marshal_with, abort, fields, marshal


artist_args = reqparse.RequestParser()
artist_args.add_argument('name', type = str, required = True, help = 'Name of artist is needed')
artist_args.add_argument('nationality', type = str, required = True, help = 'Nationality of artist is needed')
artist_args.add_argument('year_formed', type = int, help = 'Year the artist came to fruition')


artistFields = {
    'id':fields.Integer,
    'name':fields.String,
    'nationality':fields.String,
    'year_formed':fields.Integer
    }

class ArtistResource(Resource):
    # Get Artist details
    #@marshal_with(artistFields)
    def get(self, artist_id = None):
        if artist_id:
            # look for specified artist
            this_artist = Artist.query.filter_by(id = artist_id).first()
            if not this_artist:
                abort(404, message = 'Artist not found')
            return marshal(this_artist, artistFields)
        
        # show all artists
        all_artists = Artist.query.all()
        if not all_artists:
            return {"message": "No artists found"}, 200
        return marshal(all_artists, artistFields)
    
    # Add a new artist
    @marshal_with(artistFields)
    def post(self):
        args = artist_args.parse_args()
        # Check if the artist already exists
        existing_artist = Artist.query.filter_by(name=args['name']).first()
        if existing_artist:
            abort(400, message='Artist with this name already exists')        

        new_artist = Artist(name = args["name"],
        nationality = args["nationality"],
        year_formed = args["year_formed"])
        
        db.session.add(new_artist)
        db.session.commit()
        #artists = Artist.query.all()
        return new_artist, 201
    
    # Delete an artist
    def delete(self, artist_id):

        """
        Deletes artist based on artist ID.

        Args:
            artist_id (int): ID of the specific artist to remove.

        Returns:
            Name of artist deleted.
        """

        artist = Artist.query.filter_by(id = artist_id).first()
        if not artist:
            abort(http_status_code=404, message="Artist not found")
        db.session.delete(artist)
        db.session.commit()
        return {'message': f'Artist {artist.name} was successfully deleted'}, 200
    

    # Update an artist's details
    @marshal_with(artistFields)
    def put(self, artist_id):

        """
        Modifies artist details based on artist ID.

        Args:
            artist_id (int): ID of the specific artist to modify.

        Returns:
            Details of newly modified artist.
        """

        artist = Artist.query.get(artist_id)
        if not artist:
           abort(404, message = 'Artist not found')

        args = artist_args.parse_args()
        

        # Only update fields that were provided
        if args['name']:
            artist.name = args['name']
        if args['nationality']:
            artist.nationality = args['nationality']
        if args['year_formed']:
            artist.year_formed = args['year_formed']        
    
        #artist.name = args['name']
        #artist.nationality = args["nationality"]
        #artist.year_formed = args["year_formed"]
        
        db.session.commit()
        #artists = Artist.query.all()
        return artist, 200
        
