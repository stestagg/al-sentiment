#!/usr/bin/env python

"""
Usage: server.py [options]

Options:
 --port=<port>    Run the webserver on the specified port [default: 5000]
 -d, --debug      Run the webserver in debug mode (not safe)
 -l <host>, --listen=<host>  Bind the webserver to this address
                             [default: 127.0.0.1]
 -f, --database=<db>  Path to the SQLite database file [default: :memory:]
"""

import sys

import docopt
import flask

import sentiment.models


app = flask.Flask(__name__)


@app.route("/_ping")
def ping():
    """Simple endpoint for aliveness testing"""
    return "PONG"


@app.route("/")
def index():
    """Displays the main page HTML, other resources are fetched via JSON"""
    return flask.render_template("index.html")


def main():
    options = docopt.docopt(__doc__)
    try:
        port = int(options["--port"])
    except ValueError:
        usage("Port must be an integer")

    # Connect to the right Database
    sentiment.models.setup(options["--database"])
    app.run(port=port, host=options["--listen"], debug=options["--debug"])


if __name__ == "__main__":
    sys.exit(main())
