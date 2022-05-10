"""
This is the API server for the WebQuiz Web App.
It provides an API so that the Web frontend and other potential clients
can access WebQuiz storage and services.

(c) Joao Galamba, 2022
$LICENSE(MIT)
"""

from flask import Flask, request, session
from flask_cors import CORS

from . import db
from .utils import snake_to_camel_case

################################################################################
##
##      FLASK SERVER INIT
##
################################################################################

def create_app(test_config=None):
    """
    Factory function used to create the flask/server app. Loosely 
    based on the tutorial: 
    https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/
    See:
    https://flask.palletsprojects.com/en/2.1.x/config/#builtin-configuration-values
    """

    ############################################################################
    ##
    ##      APPLICATION INITIALIZATION
    ##
    ############################################################################

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    flask_env = app.config.get('ENV', 'production')
    print(f"\n\n[+] STARTED IN {flask_env.upper()} MODE\n\n")

    # https://flask.palletsprojects.com/en/2.1.x/config/
    if test_config:
        app.config.from_mapping(test_config)
        print("[+] Loaded configuration from a DICT like object!")
    else:
        config_type = flask_env.capitalize()
        app.config.from_object(f'instance.config.{config_type}')
        print(f"[+] Loaded configuration '{config_type}' from CONFIG.PY")

    USER_NOT_FOUND = 'null'
    DEBUG = app.config['DEBUG']
    if DEBUG:
        print(f"{app.config['TESTING']=}")
        print(f"{app.config['SESSION_COOKIE_NAME']=}")
        print(f"{app.config['DATABASE']=}")
        print(f"{app.config['DATABASE_HOST']=}")
        print(f"{app.config['DATABASE_USER']=}")

    db.init_db_connector(
        host = app.config['DATABASE_HOST'],
        database = app.config['DATABASE'],
        user = app.config['DATABASE_USER'],
        password = app.config['DATABASE_PASSWORD'],
    )
    print("[+] Initialized DB CONNECTOR")

    ############################################################################
    ##
    ##      ROUTES RELATED TO USER AND SESSION MANAGEMENT
    ##
    ############################################################################

    @app.route("/user/login", methods=['POST'])
    def login():
        login_data = request.get_json()
        username = login_data['username']
        password = login_data['password']
        if (user := db.authenticate_user(username, password, snake_to_camel_case)):
            session.clear()
            session['userid'] = user['id']
            session.permanent = True
            return user
        return USER_NOT_FOUND
    #:

    @app.route("/user/login", methods=['DELETE'])
    def logout():
        session.clear()
        return ''
    #:

    @app.route("/user/current", methods=['GET'])
    def get_current_user():
        userid = session.get('userid')
        if (user := db.get_user_info(userid, snake_to_camel_case)):
            return user
        return USER_NOT_FOUND
    #:

    @app.route("/user/current", methods=['POST'])
    def create_user():
        # userid = session.get('userid')
        user_data = request.get_json()
        print('[+] CREATING USER:', user_data)
        return USER_NOT_FOUND
    #:

    ############################################################################
    ##
    ##      ROUTES FOR TESTING AND DEBUGGING PURPOSES
    ##
    ############################################################################

    if DEBUG:
        @app.route("/_login-form", methods=['GET'])
        def _login_form():
            return '''\
        <form method="POST" action="/login-test">
            <div><label>Username:</label><input type="text" name="username"></div>
            <div><label>Password:</label><input type="password" name="password"></div>
            <input type="submit" value="Submit">
        </form>
        '''
        #:

        @app.route("/_login", methods=['POST'])
        def _login_test():
            username = request.form.get('username')
            pwd = request.form.get('password')
            if username == 'alb' and pwd == 'abc':
                return '<h1>Welcome back Alberto</h1>'
            return f'<h1>Unknown user {username}</h1>'
        #:

    return app
#: CREATE_APP

# @app.route("/user/login", methods=['POST'])
# def login():
#     login_info = request.get_json()
#     username = login_info['username']
#     pwd = login_info['password']
#     if username == 'alb' and pwd == 'abc':
#         return {'username': username, 'name': 'Alberto Antunes'}
#     return USER_NOT_FOUND
# #:

# @app.route("/hello/<name>")
# def hello_there(name):
#     now_txt = datetime.now().strftime("%A, %d %B, %Y at %X")

#     # Filter the name argument to letters only using regular expressions. URL arguments
#     # can contain arbitrary text, so we restrict to safe characters only.
#     clean_name = "Friend"
#     match_object = re.match("[a-zA-Z]+", name)
#     if match_object:
#         clean_name = match_object.group(0)

#     return f"<p>Hello there, {clean_name}! It's {now_txt}</p>"
# #:

# @app.route("/")
# def home():
#     return {
#         'message': 'This the WebQuizz backend. You probably want to call one of the API methods.'
#     }
# #:

# DATABASE LINKS
# https://tecadmin.net/how-to-install-mysql-server-on-ubuntu-22-04/
