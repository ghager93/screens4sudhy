import os
import shutil

from flask import Blueprint, request

from app.core import take_all_screenshots, take_screenshots


bp = Blueprint("take_screenshots", __name__)


@bp.route("/all", methods=["PUT"])
def trigger_take_all_screenshots():
    """
    Take screenshots of all saved urls. Add them to dated folder.
    TODO Add query option to select destination folder?
    """
    try:
        take_all_screenshots()
        return "Screenshots successfully created", 200
    except:
        return "An error occurred", 500


@bp.route("/", methods=["PUT"])
def trigger_take_screenshots():
    """
    Take screensohts of urls specified in http body.
    """
    body = request.get_json()
    if "urls" not in body:
        return "No urls specified", 400

    directory = take_screenshots(body["urls"])

    return {
        "dir": directory,
        "urls": body["urls"]
    }, 200


@bp.route("/", methods=["DELETE"])
def delete_screenshots():
    if "all" in request.args and request.args["all"] == "true":
        _delete_all_screenshots()
        return "Deleted all screenshots", 200


def _delete_all_screenshots():
    for root, dirs, files in os.walk('screenshots'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
