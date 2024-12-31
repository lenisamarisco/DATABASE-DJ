from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField('Song Title', validators=[DataRequired(), Length(min=1, max=100)])
    artist = StringField('Artist', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Add Song')
