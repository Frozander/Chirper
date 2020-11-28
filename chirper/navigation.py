"""
Chiper.Navigation

This module creates and renders the Navbar on the site using flask-nav
"""

from flask_bootstrap.nav import BootstrapRenderer
from flask_login import current_user
from flask_nav import Nav
from flask_nav.elements import Navbar, View


class CustomRenderer(BootstrapRenderer):
    """
    A custom renderer that adds the neccesary bootstrap tags to the navbar
    """

    def visit_Navbar(self, node):
        nav_tag = super(CustomRenderer, self).visit_Navbar(node)
        nav_tag['class'] += 'navbar navbar-inverse navbar-fixed-top'
        return nav_tag


nav = Nav()

# Views
home_view = View('Chirper', 'index')
login_view = View('Log In', 'auth.login')
register_view = View('Register', 'auth.register')
logout_view = View('Logout', 'auth.logout')
create_post_view = View('Post', 'posts.create')


@nav.navigation('chirper_navbar')
def create_navbar():
    """
    create_navbar() -> Navbar
    Creates a Navbar according to the user
    """

    views = [home_view]
    if current_user.is_authenticated:
        profile_view = View('Profile', 'user.profile',
                            user_id=current_user.id)
        views.append(create_post_view)
        views.append(profile_view)
        views.append(logout_view)
    else:
        views.append(register_view)
        views.append(login_view)

    return Navbar(*views)
