import os
import logging

from flask import Flask, send_file

from app import core


app = Flask(__name__)

# @app.route("/healthcheck", methods=["GET"])
# def healthcheck():
#     logging.info("This is a healthcheck log.")
#     return "", 200


# @app.route("/screenshots", methods=["GET"])
# def get_screenshots():
#     try:
#         core.main_multithread()
#         return "Screenshots successfully created", 200
#     except:
#         return "An error occurred", 500

from app.api import healthcheck
from app.api import take_screenshots
from app.api import download

app.register_blueprint(healthcheck.bp, url_prefix="/api/healthcheck")
app.register_blueprint(take_screenshots.bp, url_prefix="/api/screenshots")
app.register_blueprint(download.bp, url_prefix="/api/download")

@app.route("/downloadtest", methods=["GET", "POST"])
def download_test():
    path = os.path.join(app.root_path, "core.py")
    return send_file(path, as_attachment=True)

