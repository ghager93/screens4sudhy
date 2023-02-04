import logging

from flask import Flask

from . import core


app = Flask(__name__)

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    logging.info("healthcheck")
    return 200


@app.route("/screenshots", methods=["GET"])
def get_screenshots():
    try:
        core.main_multithread()
        return "Screenshots successfully created", 200
    except:
        return "An error occurred", 500     

