'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import sql
from bottle import request, response

# Initialise our views, all arguments are defaults for the template
page_view = view.View()


# -----------------------------------------------------------------------------
# Cookie
# -----------------------------------------------------------------------------
def get_cookie():
    username = request.get_cookie('username', secret='usafe')
    password = request.get_cookie('password', secret='psafe')
    role = request.get_cookie('role', secret='rsafe')
    return (username, password, role)


def set_cookie(username, password, role, max_age=600):
    response.set_cookie('username', username, secret='usafe', max_age=max_age)
    response.set_cookie('password', password, secret='psafe', max_age=max_age)
    response.set_cookie('role', role, secret='rsafe', max_age=max_age)


def clr_cookie():
    set_cookie(None, None, None, max_age=1)

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------


def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

# -----------------------------------------------------------------------------
# Login
# -----------------------------------------------------------------------------


def load_login():
    # Getting cookie from the user
    username, password, role = get_cookie()

    # Check the cookie
    result = sql.userbase.check_credentials(username, password)
    if result != None:
        if result == 1:
            role = "Admin"
        elif result == 0:
            role = "User"
        else:
            role = "Nobody"
        return logged_in(username, role)
    else:
        return login_form()
# ------------------------------------------------------------------------------


def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

# ------------------------------------------------------------------------------


def logged_in(name, role):
    '''
        login_form
        Returns the view for the logged_in page
    '''
    return page_view("logged_in", name=name, role=role)

# -----------------------------------------------------------------------------

# Check the login credentials


def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    result = sql.userbase.check_credentials(username, password)
    if result != None:
        if result == 1:
            role = "Admin"
        elif result == 0:
            role = "User"
        else:
            role = "Nobody"
        set_cookie(username, password, result)
        return page_view("valid", name=username, role=role)
    else:
        return page_view("invalid", reason="Invalid name or password")

# -----------------------------------------------------------------------------

def logout():
    '''
    logout this account
    back to login page
    '''

    clr_cookie()
    return page_view("login")

# -----------------------------------------------------------------------------
def register():
    '''
    Jump to register page

    '''

    return page_view("register")


# -----------------------------------------------------------------------------
# def back_to_home():
#     '''
#     Jump back to home page
#
#     '''
#
#     return page_view("home")
#

# ------------------------------------------------------------------------------
def new_account_add(username, password):
    '''
    Add new user into database

    '''
    if(username != None and password != None):
        sql.userbase.add_user(username, password)
        result = sql.userbase.check_credentials(username, password)
        if result != None:
            if result == 1:
                role = "Admin"
            elif result == 0:
                role = "User"
            else:
                role = "Nobody"
            set_cookie(username, password, result)
            return page_view("valid", name=username, role=role)
        else:
            return page_view("invalid", reason="Invalid name or password")

# About
# -----------------------------------------------------------------------------


def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())

# Returns a random string each time


def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = "create a better model of program language learning."
    return garble

# -----------------------------------------------------------------------------
