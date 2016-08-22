# Connect Four

While inspired by
[Connect Four](https://en.wikipedia.org/wiki/Connect_Four),
this game accommodates other numbers (Connect Three, Six, etc.),
as well as variable board dimensions and a variable number of players.


## Code

The game logic code is in Python.

Python version is listed in [runtime.txt](runtime.txt).

Package dependencies are listed in [requirements.txt](requirements.txt).
To install (preferably in a new [virtualenv](https://virtualenv.pypa.io)):
```
pip install -r requirements.txt
```

The GUI view uses Python's built-in Tkinter library.

The web view uses the [Flask](http://flask.pocoo.org/) framework, and the
WebSocket protocol to communicate between client and server
([socket.io](http://socket.io/) on the client side and
[Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) on the
server side).
The front end uses [React](https://facebook.github.io/react/)
with [Redux](http://redux.js.org/), and is packed with
[webpack](http://webpack.github.io/).


## App

To start the command line app (from root dir):
```
python commandline_app.py
```

To start the GUI app (from root dir):
```
python gui_app.py
```

To start the web app (from root dir):
```
python web_app.py
```


## Web app dev dependencies

To do development work on the web app, first install js dependencies (listed
in [package.json](package.json)):
```
npm install
```

If you install any new npm dependencies, use the `--save-dev` option to list
the new requirement in [package.json](package.json):
```
npm install <package-name> --save-dev
```

To have webpack auto-compile JS and CSS during dev:
```
webpack --watch
```


## Tests

To run all unit tests (from root dir):
```
python -m unittest discover -v
```
