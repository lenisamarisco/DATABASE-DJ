from flask_wtf.csrf import generate_csrf
from app import app
from forms import SongForm, PlaylistForm


class TestForms:
    class TestSong:
        def test_song_form_has_title_and_artist_fields(self):
            with app.test_request_context():
                form = SongForm()

                assert 'title' in form.data
                assert 'artist' in form.data

        def test_song_form_doesnt_include_unexpected_fields(self):
            with app.test_request_context():
                form = SongForm()
                form.title.data = 'sample-title'
                form.artist.data = 'sample-artist'
                form.csrf_token.data = generate_csrf()  # Set CSRF token

                keys = list(form.data.keys())

                # Remove 'title', 'artist', and '_csrf' token keys from the keys list
                keys.remove('title')
                keys.remove('artist')
                keys.remove('csrf_token')

                # Check if there are any keys remaining in the list
                assert keys == [
                ], f"Unexpected fields found in the SongForm: {', '.join(keys)}"

        def test_song_form_validation_is_working(self):
            with app.test_request_context(method="POST"):
                form = SongForm()
                form.title.data = ''
                form.artist.data = ''
                form.csrf_token.data = generate_csrf()
                assert form.validate_on_submit() is False

                form.title.data = 'new-title'
                form.artist.data = 'new-artist'
                form.csrf_token.data = generate_csrf()
                assert form.validate_on_submit() is True

    class TestPlaylist:
        def test_playlist_form_includes_name_and_description_fields(self):
            with app.test_request_context():
                form = PlaylistForm()

                assert 'name' in form.data
                assert 'description' in form.data

        def test_playlist_form_doesnt_include_unexpected_fields(self):
            with app.test_request_context():
                form = PlaylistForm()
                form.name.data = 'sample-name'
                form.description.data = 'sample-description'
                form.csrf_token.data = generate_csrf()  # Set CSRF token

                keys = list(form.data.keys())

                # Remove 'title', 'artist', and '_csrf' token keys from the keys list
                keys.remove('name')
                keys.remove('description')
                keys.remove('csrf_token')

                # Check if there are any keys remaining in the list
                assert keys == [
                ], f"Unexpected fields found in the PlaylistForm: {', '.join(keys)}"

        def test_playlist_form_validation_is_working(self):
            with app.test_request_context(method="POST"):
                form = PlaylistForm(name='', description='')
                form.csrf_token.data = generate_csrf()
                assert form.validate_on_submit() is False

                form = PlaylistForm(name='test', description='test')
                form.csrf_token.data = generate_csrf()
                assert form.validate_on_submit() is True
