#!/usr/bin/env python

"""
Usage: server.py [options]

Options:
 --port=<port>    Run the webserver on the specified port [default: 5000]
 -d, --debug      Run the webserver in debug mode (not safe)
 -l <host>, --listen=<host>  Bind the webserver to this address
                             [default: 127.0.0.1]
 -f, --database=<db>  Path to the SQLite database file [default: :memory:]
 --feed=<url>     URL for twitter data feed
"""

import sys

import docopt
import flask

import sentiment.models
import sentiment.feed


app = flask.Flask(__name__)


@app.route("/_ping")
def ping():
    """Simple endpoint for aliveness testing"""
    return "PONG"


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/update")
def update():
    """Fetch more tweets from the feed.  WARNING: this request may block
    for a long time, which may cause problems with concurrency"""
    result = sentiment.feed.fetch_tweets()
    is_success = result is None
    return flask.jsonify({"success": is_success, "message": result})


@app.route("/tweets")
def get_tweets():
    return flask.render_template(
        "tweets.html", tweets=sentiment.models.Tweet.by_sentiment())


def main():
    options = docopt.docopt(__doc__)
    try:
        port = int(options["--port"])
    except ValueError:
        usage("Port must be an integer")

    # TODO: update the feed url based on options
    # Connect to the right Database
    sentiment.models.setup(options["--database"])
    app.run(port=port, host=options["--listen"], debug=options["--debug"])


if __name__ == "__main__":
    sys.exit(main())
