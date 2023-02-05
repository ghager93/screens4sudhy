import logging

from flask import Blueprint


bp = Blueprint("healthcheck", __name__)


@bp.route("/", methods=["GET"])
def healthcheck():
    logging.info("This is a healthcheck log.")
    return "", 200
