from forms import SongForm # type: ignore
from app import app # type: ignore
from flask_wtf.csrf import generate_csrf

def test_song_form_submission(client):
    form = SongForm(title="New Song", artist="Artist Name")
    form.csrf_token.data = generate_csrf()  # Add CSRF token to avoid errors
    
    assert form.validate_on_submit() is True  # Validate the form submission
    # Simulate a POST request to submit the form
    response = client.post('/add-song', data=form.data)
    assert response.status_code == 200  # Success response
    assert b'Song added successfully' in response.data  # Confirm the success message is in the response
