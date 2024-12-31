import os
import pytest
from app import app, db, Playlist, Song  # type: ignore # Import your Flask app, db, and models
from flask import Flask

# Configure Flask app for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'  # Make sure to use the test database if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True  # Enable testing mode
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"  # Set a secret key for testing

# Initialize the app's test client
@pytest.fixture
def client():
    """Fixture for test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def setup_db():
    """Fixture to set up the database before each test."""
    db.create_all()  # Create tables
    yield db  # This will allow tests to run
    db.session.remove()  # Clean up session
    db.drop_all()  # Drop tables after the test


def test_homepage(client):
    """Test the homepage redirection."""
    response = client.get('/')
    assert response.status_code == 302  # It should redirect
    assert response.location == "http://localhost/playlists"  # Redirect location


def test_show_all_playlists(client, setup_db):
    """Test the route that shows all playlists."""
    # Create some test playlists
    playlist1 = Playlist(name="Rock Classics", description="Best of rock music")
    playlist2 = Playlist(name="Pop Hits", description="Top pop songs")
    db.session.add_all([playlist1, playlist2])
    db.session.commit()

    # Test if playlists are displayed correctly
    response = client.get('/playlists')
    assert response.status_code == 200
    assert b'Rock Classics' in response.data
    assert b'Pop Hits' in response.data


def test_add_playlist(client, setup_db):
    """Test the add playlist functionality."""
    response = client.get('/playlists/add')
    assert response.status_code == 200

    # Test posting form data to add a playlist
    response = client.post('/playlists/add', data={'name': 'Indie Vibes', 'description': 'Best indie music'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Indie Vibes' in response.data  # Check if the new playlist is in the response


def test_show_playlist_detail(client, setup_db):
    """Test showing a specific playlist's details."""
    playlist = Playlist(name="Jazz Essentials", description="Smooth jazz classics")
    db.session.add(playlist)
    db.session.commit()

    response = client.get(f'/playlists/{playlist.id}')
    assert response.status_code == 200
    assert b'Jazz Essentials' in response.data
    assert b'Smooth jazz classics' in response.data


def test_add_song(client, setup_db):
    """Test adding a song."""
    playlist = Playlist(name="Classical Hits", description="Classical music masterpieces")
    db.session.add(playlist)
    db.session.commit()

    # Test posting form data to add a song
    response = client.post('/songs/add', data={'title': 'Beethoven Symphony No. 5', 'artist': 'Ludwig van Beethoven'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Beethoven Symphony No. 5' in response.data


def test_add_song_to_playlist(client, setup_db):
    """Test adding a song to a playlist."""
    playlist = Playlist(name="Rock Anthems", description="Best rock songs")
    song = Song(title="We Will Rock You", artist="Queen")
    db.session.add_all([playlist, song])
    db.session.commit()

    response = client.get(f'/playlists/{playlist.id}/add-song')
    assert response.status_code == 200

    # Add the song to the playlist
    response = client.post(f'/playlists/{playlist.id}/add-song', data={'song': song.id}, follow_redirects=True)
    assert response.status_code == 200
    assert b'We Will Rock You' in response.data  # Check if the song was added to the playlist


def test_song_detail(client, setup_db):
    """Test viewing a song's details."""
    song = Song(title="Imagine", artist="John Lennon")
    db.session.add(song)
    db.session.commit()

    response = client.get(f'/songs/{song.id}')
    assert response.status_code == 200
    assert b'Imagine' in response.data
    assert b'John Lennon' in response.data
