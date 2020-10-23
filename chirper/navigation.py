from flask_nav import Nav
from flask_nav.elements import View, Navbar
from flask import g
from flask_login import current_user

nav = Nav()

@nav.navigation('chirper_navbar')
def create_navbar():
    home_view = View('Chirper', 'index')   
    if  current_user.is_authenticated:
        logout_view = View('Logout', 'index') # index is placeholder
        return Navbar('Chirper', home_view, logout_view)
    else:
        login_view = View('Log In', 'auth.login')
        register_view = View('Register', 'auth.register')
        return Navbar(home_view, login_view, register_view)
    