from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField


class SettingsForm(FlaskForm):
    log_level_field = SelectField('Log level', choices=[('CRITICAL', 'CRITICAL'), ('ERROR', 'ERROR'), ('WARNING', 'WARNING'), ('INFO', 'INFO'), ('DEBUG', 'DEBUG')])
    log_location_field = StringField('Log location')
    location_field = StringField('Index location')
    min_index_field = IntegerField('Min size to index (in MB)')
    use_external_api_field = SelectField('External API', choices=[('omdb', 'OMDb'), ('tmdb', 'TMDb')])
    omdb_api_key_field = StringField('OMDb API key')
    tmdb_api_key_field = StringField('TMDb API key')
    web_host_field = StringField('Web host address')
    web_port_field = StringField('Web port')
    web_require_login_field = SelectField('Require login', choices=[('False', 'No'), ('True', 'Yes')])
    submit = SubmitField('Save')
    delete_index = SubmitField('Delete index')


class LoginForm(FlaskForm):
    username_field = StringField('Username')
    password_field = PasswordField('Password')
    login = SubmitField("Login")


class AddUserForm(FlaskForm):
    username_field = StringField('Username')
    password_field = PasswordField('Password')
    user_list_field = SelectField('Users', choices=[('admin', 'admin')])
    submit = SubmitField('Add')
    delete = SubmitField('Delete')


class IndexForm(FlaskForm):
    index_location = StringField("Folder to index")
    run_index = SubmitField("Run Indexing")


class SearchForm(FlaskForm):
    autocomp = StringField('Search movie', id='autocomplete')
