import pytest
from flask_wtf.csrf import generate_csrf
from app import app  # type: ignore
from forms import SongForm, PlaylistForm  # type: ignore

# Basic test class for addition and subtraction
class TestBasicMath:
    def test_addition(self):
        assert 1 + 1 == 2

    def test_subtraction(self):
        assert 2 - 1 == 1


class TestForms:
    class TestSong:
        def test_song_form_has_title_and_artist_fields(self):
            with app.test_request_context():
                form = SongForm()

                # Check if 'title' and 'artist' fields are present in the form data
                assert 'title' in form.data
                assert 'artist' in form.data

        def test_song_form_doesnt_include_unexpected_fields(self):
            with app.test_request_context():
                form = SongForm()
                form.title.data = 'sample-title'
                form.artist.data = 'sample-artist'
                form.csrf_token.data = generate_csrf()  # Set CSRF token

                keys = list(form.data.keys())

                # Remove 'title', 'artist', and '_csrf_token' token keys from the keys list
                keys.remove('title')
                keys.remove('artist')
                keys.remove('_csrf_token')  # Update this to match the actual CSRF token field name

                # Check if there are any keys remaining in the list
                assert keys == [], f"Unexpected fields found in the SongForm: {', '.join(keys)}"

        def test_song_form_validation_is_working(self):
            with app.test_request_context(method="POST"):
                form = SongForm(title='', artist='')  # Empty fields to trigger validation failure
                form.csrf_token.data = generate_csrf()
                assert form.validate_on_submit() is False

                form.title.data = 'new-title'
                form.artist.data = 'new-artist'
                form.csrf_token.data = generate_csrf()  # Valid data to trigger success
                assert form.validate_on_submit() is True

    class TestPlaylist:
        def test_playlist_form_includes_name_and_description_fields(self):
            with app.test_request_context():
                form = PlaylistForm()

                # Check if 'name' and 'description' fields are present in the form data
                assert 'name' in form.data
                assert 'description' in form.data

        def test_playlist_form_doesnt_include_unexpected_fields(self):
            with app.test_request_context():
                form = PlaylistForm()
                form.name.data = 'sample-name'
                form.description.data = 'sample-description'
                form.csrf_token.data = generate_csrf()  # Set CSRF token

                keys = list(form.data.keys())

                # Remove 'name', 'description', and '_csrf_token' token keys from the keys list
                keys.remove('name')
                keys.remove('description')
                keys.remove('_csrf_token')  # Update to match the CSRF field name in your form

                # Check if there are any keys remaining in the list
                assert keys == [], f"Unexpected fields found in the PlaylistForm: {', '.join(keys)}"

        def test_playlist_form_validation_is_working(self):
            with app.test_request_context(method="POST"):
                form = PlaylistForm(name='', description='')  # Empty fields to trigger validation failure
                form.csrf_token.data = generate_csrf()
                assert form.validate_on_submit() is False

                form = PlaylistForm(name='test', description='test')
                form.csrf_token.data = generate_csrf()  # Valid data to trigger success
                assert form.validate_on_submit() is True
