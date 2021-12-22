import json
import logging

import flask
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wrappers import Response

from . import board


def _init_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


_init_logging()


def log_http_exception(e: HTTPException):
    if not isinstance(e, HTTPException):
        logging.exception("Unexpected exception")
        return Response(status=500)

    if not isinstance(e, NotFound):
        logging.exception(
            "Encountered an error while processing a %s request to %s with payload %s",
            flask.request.method,
            flask.request.base_url,
            flask.request.data,
        )
    response = e.get_response()
    response.data = json.dumps({"description": e.description})
    response.set_content_type = "application/json"
    return response


def create_app():
    app = flask.Flask("mines")
    app.register_error_handler(HTTPException, log_http_exception)

    app.add_url_rule("/games", methods=["POST"], view_func=board.create_board)
    app.add_url_rule(
        "/games/<int:game_id>/guesses", methods=["POST"], view_func=board.uncover_tile
    )
    app.env = "development"
    app.debug = True
    return app
