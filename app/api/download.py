import os

from flask import Blueprint, request, send_from_directory, send_file

from app.core import get_todays_path


bp = Blueprint("download", __name__)


@bp.route("/today", methods=["GET", "POST"])
def download_todays():
    todays_path = get_todays_path()
    if not os.path.exists(todays_path) or not os.listdir(todays_path):
        return "No screenshots created today", 400
    
    file = os.path.join("../", todays_path, os.listdir(todays_path)[0])
    return send_file(file, as_attachment=True)
