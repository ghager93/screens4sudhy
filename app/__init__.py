import os
import logging

from flask import Flask, send_file, request

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

@app.route("/")
def list_dir():
    exclude = ["__pycache__", "venv", ".git"]
    
    walk = ""
    for root, dirs, files in os.walk(".", topdown=False):
        if any([e in root for e in exclude]):
            continue
        [dirs.remove(d) for d in dirs if d in exclude]
        for name in files:
            walk += os.path.join(root, name) + '\n'
        for name in dirs:
            walk += os.path.join(root, name) + '\n'

    return walk, 200


@app.route("/pagesource")
def get_google_pagesource():
    if "driver_path" in request.args:
        driver_path = request.args.get("driver_path")
    webdriver = core.get_chrome_driver(driver_path)
    webdriver.get("https://google.com")
    return webdriver.page_source, 200


@app.route("/pagesourcemanager")
def get_google_pagesource_manager():
    webdriver = core.get_chrome_driver_from_manager()
    webdriver.get("https://google.com")
    return webdriver.page_source, 200


@app.route("/pagesourcedocker")
def get_google_pagesource_docker():
    webdriver = core.get_remote_chrome_driver()
    webdriver.get("https://google.com")
    return webdriver.page_source, 200
