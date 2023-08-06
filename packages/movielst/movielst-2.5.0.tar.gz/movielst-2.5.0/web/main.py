from flask import Flask, render_template, send_from_directory, send_file, session, request, redirect, Response
import json
import subprocess
import re
from movielst import config, database
from web.forms import SettingsForm, LoginForm, AddUserForm, IndexForm, SearchForm
from web.dependency import check_for_dep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'not really secret but still a really useless secret key for this use case'
app.config['DEP_FOLDER'] = config.CONFIG_PATH + 'dep/'
app.config['CACHE_FOLDER'] = config.CONFIG_PATH + 'cache/'

regex_url_valid = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def main():
    check_for_dep()
    app.run(host=config.get_setting('Web', 'host'), port=config.get_setting('Web', 'port'), debug=False)


@app.route('/api/v1/dep/<path:filename>', methods=["GET"])
def dep_files(filename):
    return send_from_directory(app.config['DEP_FOLDER'], filename=filename)


@app.route('/api/v1/cache/<path:filename>', methods=["GET"])
def cached_image_file(filename):
    return send_from_directory(app.config['CACHE_FOLDER'], filename=filename)


@app.route('/api/v1/autocomplete', methods=['GET'])
def autocomplete():
    movie_names_json = database.db_to_json()
    movie_names = []
    for i in movie_names_json:
        movie_names.append(i['title'])
    return Response(json.dumps(movie_names), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in') and config.get_setting('Web', 'require_login') == "True":
        return login()
    else:
        form = IndexForm()
        error = None
        cached = False
        data = database.db_to_json()
        if not data:
            data = None
        if form.validate_on_submit():
            if form.run_index.data:
                output = subprocess.check_output('movielst ' + form.index_location.data)
                if "Directory does not exists." in str(output):
                    error = "invalid directory"
                else:
                    return redirect('/')
        form.process()
        search_form = SearchForm(request.form)
        if data is not None:
            for movie in data:
                if re.match(regex_url_valid, movie["poster"]):
                    # is a valid url, return cached False, ie. do nothing
                    cached = False
                else:
                    # Is not a url, return cached True to show local file instead#
                    cached = True
        return render_template('home.html', movie_list=data, form=form, error=error, cached=cached, search=search_form)


@app.route('/movie/<variable>')
def movie(variable):
    if not session.get('logged_in') and config.get_setting('Web', 'require_login') == "True":
        return login()
    else:
        data = database.db_to_json()
        i = 0
        list = {}
        for datas in data:
            if datas["title"] == variable:
                list["title"] = datas["title"]
                list["genre"] = datas["genre"]
                list["imdb"] = datas["imdb"]
                list["runtime"] = datas["runtime"]
                list["tomato"] = datas["tomato"]
                list["year"] = datas["year"]
                list["awards"] = datas["awards"]
                list["cast"] = datas["cast"]
                list["director"] = datas["director"]
                list["poster"] = datas["poster"]
                if re.match(regex_url_valid, list["poster"]):
                    cached = False
                else:
                    list["poster"] = list["poster"].replace(config.CONFIG_PATH + 'cache/', '')
                    cached = True

                list["description"] = datas["description"]
            i += 1
        return render_template('movie.html', list=list, cached=cached)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session.get('logged_in') and config.get_setting('Web', 'require_login') == "True":
        return login()
    else:
        form = SettingsForm()
        form.log_level_field.default = config.get_setting('General', 'log_level')
        form.log_location_field.default = config.get_setting('General', 'log_location')
        form.location_field.default = config.get_setting('Index', 'location')
        form.min_index_field.default = config.get_setting('Index', 'min_size_to_index')
        form.use_external_api_field.default = config.get_setting('API', 'use_external_api')
        form.omdb_api_key_field.default = config.get_setting('API', 'OMDb_API_key')
        form.tmdb_api_key_field.default = config.get_setting('API', 'TMdb_API_key')
        form.web_host_field.default = config.get_setting('Web', 'host')
        form.web_port_field.default = config.get_setting('Web', 'port')
        form.web_require_login_field.default = config.get_setting('Web', 'require_login')
        if form.validate_on_submit():
            config.update_config('General', 'log_level', form.log_level_field.data)
            config.update_config('General', 'log_location', form.log_location_field.data)
            config.update_config('Index', 'location', form.location_field.data)
            config.update_config('Index', 'min_size_to_index', str(form.min_index_field.data))
            config.update_config('API', 'use_external_api', form.use_external_api_field.data)
            config.update_config('API', 'OMDb_API_key', form.omdb_api_key_field.data)
            config.update_config('API', 'TMdb_API_key', form.tmdb_api_key_field.data)
            config.update_config('Web', 'host', form.web_host_field.data)
            config.update_config('Web', 'port', form.web_port_field.data)
            config.update_config('Web', 'require_login', form.web_require_login_field.data)
            if form.delete_index.data:
                database.delete_all_movies()
        form.process()
        return render_template('settings/settings.html', form=form)


@app.route('/settings/users', methods=['GET', 'POST'])
def settings_user():
    if not session.get('logged_in') and config.get_setting('Web', 'require_login') == "True":
        return login()
    else:
        form = AddUserForm()
        choices_list = [(i[0], i[0]) for i in database.get_users()]
        form.user_list_field.choices = choices_list

        if form.validate_on_submit():
            if form.submit.data:
                # Add user to database
                database.add_user(form.username_field.data, form.password_field.data)
            if form.delete.data:
                database.delete_user(form.user_list_field.data)
        form.process()
        return render_template('settings/users.html', form=form)


@app.route('/export/<type>/<name>')
def export(type, name):
    if not session.get('logged_in') and config.get_setting('Web', 'require_login') == "True":
        return login()
    else:
        if type == 'csv':
            database.export_to_csv(config.CONFIG_PATH + name)
            return send_file(config.CONFIG_PATH + name, as_attachment=True)
        elif type == 'xlsx':
            database.export_to_xlsx(config.CONFIG_PATH + name)
            return send_file(config.CONFIG_PATH + name, as_attachment=True)
        else:
            return "File type not supported"


@app.route('/movie/play/<variable>')
def play(variable):
    return send_from_directory('/', variable)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if  database.verify_user(form.username_field.data, form.password_field.data):
                session['logged_in'] = True
                return redirect('/')
            else:
                print("login failed")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')


if __name__ == '__main__':
    main()
