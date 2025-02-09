<<<<<<< HEAD
from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import os

from forms import NewSongForPlaylistForm, SongForm, PlaylistForm  # type: ignore

# Initialize the Flask app
app = Flask(__name__)

# App config for database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///playlist-app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"  # Set a secret key for sessions

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)  # Initialize db after configuring app

# Initialize Debug Toolbar
debug = DebugToolbarExtension(app)

# Models for Playlist App
=======
"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

>>>>>>> fdfed954150e02c990de45cb7f20c98a66cad5cc

class Playlist(db.Model):
    """Playlist."""

<<<<<<< HEAD
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    songs = db.relationship('Song', secondary='playlist_song', back_populates='playlists')

    def __repr__(self):
        return f'<Playlist {self.name}>'
=======
    # ADD THE NECESSARY CODE HERE
>>>>>>> fdfed954150e02c990de45cb7f20c98a66cad5cc


class Song(db.Model):
    """Song."""

<<<<<<< HEAD
    __tablename__ = 'songs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    
    playlists = db.relationship('Playlist', secondary='playlist_song', back_populates='songs')

    def __repr__(self):
        return f'<Song {self.title} by {self.artist}>'
=======
    # ADD THE NECESSARY CODE HERE
>>>>>>> fdfed954150e02c990de45cb7f20c98a66cad5cc


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

<<<<<<< HEAD
    __tablename__ = 'playlist_song'
    
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)
    
    playlist = db.relationship(Playlist, back_populates='songs')
    song = db.relationship(Song, back_populates='playlists')

    def __repr__(self):
        return f'<PlaylistSong playlist_id={self.playlist_id} song_id={self.song_id}>'

# Initialize the database (migrate)
@app.before_first_request
def create_tables():
    db.create_all()

# Routes for the Flask application

@app.route('/')
def home():
    """Homepage."""
    return 'Welcome to the Playlist App!'

@app.route('/playlists')
def show_all_playlists():
    """Return a list of playlists."""
    playlists = Playlist.query.all()
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlists/<int:playlist_id>')
def show_playlist(playlist_id):
    """Show details of a specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    songs = playlist.songs
    return render_template('playlist_detail.html', playlist=playlist, songs=songs)

@app.route('/playlists/add', methods=['GET', 'POST'])
def add_playlist():
    """Handle add-playlist form."""
    form = PlaylistForm()
    if form.validate_on_submit():
        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        db.session.add(new_playlist)
        db.session.commit()
        flash('Playlist added successfully!')
        return redirect('/playlists')
    return render_template('add_playlist.html', form=form)

@app.route('/songs')
def show_all_songs():
    """Return a list of songs."""
    songs = Song.query.all()
    return render_template('songs.html', songs=songs)

@app.route('/songs/<int:song_id>')
def show_song(song_id):
    """Show details of a specific song."""
    song = Song.query.get_or_404(song_id)
    return render_template('song_detail.html', song=song)

@app.route('/songs/add', methods=['GET', 'POST'])
def add_song():
    """Handle add-song form."""
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(new_song)
        db.session.commit()
        flash('Song added successfully!')
        return redirect('/songs')
    return render_template('add_song.html', form=form)

@app.route('/playlists/<int:playlist_id>/add-song', methods=['GET', 'POST'])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    existing_song_ids = [song.id for song in playlist.songs]
    form.song.choices = [(song.id, song.title) for song in Song.query.all() if song.id not in existing_song_ids]

    if form.validate_on_submit():
        song = Song.query.get(form.song.data)
        playlist.songs.append(song)
        db.session.commit()
        flash(f"Song '{song.title}' added to playlist '{playlist.name}'!")
        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)

if __name__ == "__main__":
    app.run(debug=True)
=======
    # ADD THE NECESSARY CODE HERE


# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
>>>>>>> fdfed954150e02c990de45cb7f20c98a66cad5cc
