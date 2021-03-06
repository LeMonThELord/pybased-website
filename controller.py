'''
    This file will handle our typical Bottle requests and responses
    You should not have anything beyond basic page loads, handling forms and
    maybe some simple program logic
'''

from bottle import route, get, post, static_file, request

import model

# -----------------------------------------------------------------------------
# Static file paths
# -----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

# -----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

# -----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index

        Serves the index page
    '''
    return model.index()

# -----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.load_login()

# -----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')

    # Call the appropriate method
    return model.login_check(username, password)

# -----------------------------------------------------------------------------
@post('/valid')
def post_valid():
    '''
    After logged in
    Back to index page.

    '''
    # back = request.button.get("My homepage")
    # if back is not None:
    return model.back_to_index()


# -----------------------------------------------------------------------------
@get('/about')
def get_about():
    '''
        get_about

        Serves the about page
    '''
    return model.about()

# -----------------------------------------------------------------------------
# Display the register page
@get('/register')
def get_register():
    '''
        get register page
    '''
    return model.register()

# -----------------------------------------------------------------------------
# Attempt to register

@post('/register')
def register_post():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return model.new_account_add(username, password)

# -----------------------------------------------------------------------------

# Display the message page
@get('/message')
def get_message_controller():
    '''
        get_message

        Serves the message page
    '''
    return model.message_form()


# -----------------------------------------------------------------------------
# Logout
@get('/logout')
def log_out():
    '''
        logout from this account
    '''
    return model.logout()

# -----------------------------------------------------------------------------
# Logout
@post('/logout')
def log_out():
    '''
        Back to login page
    '''
    return model.login_form()
