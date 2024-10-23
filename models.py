from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(70), nullable = False)
    nationality = db.Column(db.String(70), nullable = False)
    year_formed = db.Column(db.Integer)
    albums = db.relationship('Album', back_populates = 'artist', cascade = 'delete, all, delete-orphan', lazy = 'dynamic')
    #player = db.relationship('player', backref = 'team', cascade = 'delete, all, delete-orphan')


class Track(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(75), nullable = False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable = False)
    #playlists = db.relationship('Playlist', secondary = 'playlist_tracks', backref = 'track_list', overlaps = 'playlists')
    album = db.relationship('Album', back_populates = 'tracks')
    
#    playlists = db.relationship('Playlist', secondary = 'playlist_tracks', backref = 'tracks', cascade = 'all, delete', overlaps = 'playlists, track_list')

class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(75), nullable = False)
    release_date = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable = False)
    artist = db.relationship('Artist', back_populates = 'albums')
    tracks = db.relationship('Track', back_populates = 'album', lazy = True)
 
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(70), nullable = False)
    tracks = db.relationship('Track', secondary = 'playlist_tracks', backref = 'playlists')

#    tracks = db.relationship('Track', secondary = 'playlist_tracks', backref = 'playlists', cascade = 'all, delete', overlaps = 'track_list, playlists')


# This is the many to mant relationship table between tracks and playlists
playlist_tracks = db.Table('playlist_tracks', 
                           db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key = True),
                           db.Column('track_id', db.Integer, db.ForeignKey('track.id'), primary_key = True))
