from flask import Flask

from screens4sudhy import main_multithread


app = Flask(__name__)

@app.route("/screenshots", methods=["GET"])
def get_screenshots():
    try:
        main_multithread()
        return "Screenshots successfully created", 200
    except:
        return "An error occurred", 500     

