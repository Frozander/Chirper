from flask_nav import Nav
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import View, Navbar
from flask_login import current_user
from dominate import tags

class CustomRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_tag = super(CustomRenderer, self).visit_Navbar(node)
        nav_tag['class'] += 'navbar navbar-inverse navbar-fixed-top'
        return nav_tag

nav = Nav()

@nav.navigation('chirper_navbar')
def create_navbar():
    home_view = View('Chirper', 'index')
    if  current_user.is_authenticated:
        logout_view = View('Logout', 'auth.logout') # index is placeholder
        return Navbar('Chirper', home_view, logout_view)
    else:
        login_view = View('Log In', 'auth.login')
        register_view = View('Register', 'auth.register')
        return Navbar(home_view, login_view, register_view)
