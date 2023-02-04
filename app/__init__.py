import os
import logging

from flask import Flask, send_file

from app import core


app = Flask(__name__)

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    logging.info("This is a healthcheck log.")
    return "", 200


@app.route("/screenshots", methods=["GET"])
def get_screenshots():
    try:
        core.main_multithread()
        return "Screenshots successfully created", 200
    except:
        return "An error occurred", 500


@app.route("/downloadtest", methods=["GET", "POST"])
def download_test():
    path = os.path.join(app.root_path, "core.py")
    return send_file(path, as_attachment=True)

