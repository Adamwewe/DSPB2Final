import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

# Connect to app pages
from apps import homepage, overview, bridge_selector, about, contact

# Used for login/logout Flask ####################################################
from flask import Flask
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    ''' This function loads the user by user id. Typically this looks up the user from a user database.
        We won't be registering or looking up users in this example, since we'll just login using LDAP server.
        So we'll simply return a User object with the passed in username.
    '''
    return User(username)


############################################################


# colors that can be used in the Dash Layout
colors = {
    'header': '#003e82',
    'text': '#ffffff'
}

# logo
# logo = 'https://bruggencampus.nl/flevoland/wp-content/uploads/2020/09/Bruggencampus-logo-w-g-980x231.png'
logo = 'https://i.ibb.co/Z6TVKR7/BRIDGEYtm-LOGO4.png'

# footer
footer = html.Footer([
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col([html.Img(
                        src=logo,
                        height='30px')],
                        style={'marginTop': '20px'}),
                ],
                align='center',

            ),

        ],
    )], style={'color': colors['header'], 'backgroundColor': colors['header'], 'height': '75px', 'position': 'fixed',
               'width': '100%', 'bottom': '0px', 'left': '0px', 'right': '0px', 'marginBottom': '0px'})

# Navigation bar with Logo
navbarLogo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                href='/',
                                children=[html.Img(src=logo, height='60px', width='160px')]
                            )
                        ),
                    ],
                    align='center',
                ),
                href='#',
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav([
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Dashboard", href="/apps/overview"),
                            dbc.DropdownMenuItem("Sustainable Renovation Support", href="/apps/bridge_selector"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="The System",
                    ),
                    dbc.NavItem(dbc.NavLink("About", href="/apps/about")),
                    dbc.NavItem(dbc.NavLink("Contact", href="/apps/contact")),
                    dbc.NavItem(html.Div(id='user-status-div'))
                ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            )
        ]
    ),
    color=colors["header"],
    dark=True,
    style={'marginBottom': '0px !important'}
)

# login view
login = html.Div([dcc.Location(id='url_login', refresh=True),

                  dbc.Container(id='login-prompt', className='form-signin', children=
                  [
                      dbc.Row([

                          dbc.Col(
                              dbc.Container([
                                  # dbc.Form([

                                  # email
                                  html.Div([
                                      dbc.Label("Username", html_for="example-username"),
                                      dcc.Input(placeholder='Enter your username',
                                                type='text', id='uname-box'),
                                  ], style={'padding': '10px', 'marginTop': '20px'}),

                                  # password
                                  html.Div([
                                      dbc.Label("Password", html_for="example-password"),
                                      dcc.Input(placeholder='Enter your password',
                                                type='password', id='pwd-box'),
                                  ], style={'padding': '10px'}),

                                  html.Div([
                                      dbc.Button('Login', color='dark', id='login-button', n_clicks=0, type='submit')
                                  ], style={'padding-top': '30px', 'paddingBottom': '30px'}),

                                  # ]),
                              ]),

                              width={'size': 6, 'offset': 3}
                          )

                      ])

                  ]),

                  html.Div(children='', id='output-state'),

                  ])

# successful login
success = html.Div([html.Div([html.H2('Login successful.'),
                              html.Br(),
                              #   dcc.Link('Home', href='/')
                              ])  # end div
                    ])  # end div

# failed Login
failed = html.Div([html.Div([html.H2('Log in Failed. Please try again.'),
                             html.Br(),
                             html.Div([login]),
                             dcc.Link('Home', href='/')
                             ])  # end div
                   ])  # end div

# logout
logout = html.Div([html.Div(html.H2('You have been logged out - Please login')),
                   html.Br(),
                   #    dcc.Link('Home', href='/')
                   ])  # end div


# callback function to login the user, or update the screen if the username or password are incorrect
@app.callback(
    Output('url_login', 'pathname'), Output('output-state', 'children'), [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'), State('pwd-box', 'value')])
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        # TODO: ADD USERS OR QUERY DATABASE FOR USERS
        if username == 'test' and password == 'test':
            user = User(username)
            login_user(user)
            return '/success', ''
        else:
            return '/login', 'Incorrect username or password'


app.layout = html.Div([

    navbarLogo,
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    dcc.Store(id='login-status', storage_type='session'),
    html.Div(id='page-content', children=[], style={'marginBottom': '75px'}),
    footer

])


#######################################################################################################################################
@app.callback(Output('user-status-div', 'children'), Output('login-status', 'data'), [Input('url', 'pathname')])
def login_status(url):
    ''' callback to display login/logout link in the header '''
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated \
            and url != '/logout':  # If the URL is /logout, then the user is about to be logged out anyways
        return dbc.NavLink('Logout', href="/logout"), current_user.get_id()
    else:
        return dbc.NavLink('Login', href="/login"), 'loggedout'


# Main route callback
@app.callback(Output('page-content', 'children'), Output('redirect', 'pathname'),
              [Input('url', 'pathname')])
def display_page(pathname):
    ''' callback to determine layout to return '''
    view = None
    url = dash.no_update
    if pathname == '/login':
        view = login
    elif pathname == '/success':
        if current_user.is_authenticated:
            view = bridge_selector.layout
        else:
            view = failed
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            view = homepage.layout
        else:
            view = login
            url = '/login'

    elif pathname == '/':
        view = homepage.layout
    elif pathname == '/apps/about':
        view = about.layout
    elif pathname == '/apps/contact':
        view = contact.layout
    elif pathname == '/apps/overview':
        view = overview.layout
    elif pathname == '/apps/bridge_selector':
        if current_user.is_authenticated:
            view = bridge_selector.layout
        else:
            view = 'Redirecting to login...'
            url = '/login'
    else:
        view = "404 Page Error! Please choose a link"

    return view, url


if __name__ == '__main__':
    app.run_server(debug=False)