from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

common_validators = [DataRequired()]


class PostForm(FlaskForm):
    title = StringField("Title", validators=common_validators)
    content = TextAreaField('Content', validators=common_validators)
    submit = SubmitField('Post')

