"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import os
import requests
import datetime
###
# Globals
###
app = flask.Flask(__name__)

###
# Environmental Variables
###

BREVETS_PORT = os.environ.get('BREVETS_PORT')
API_PORT = os.environ.get("API_PORT")

print("api port ", API_PORT, flush=True)
print("Brevets port", BREVETS_PORT, flush=True)

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404


@app.route("/_get_now")
def _calc_now():
    return flask.jsonify(result={"now": arrow.now().format('YYYY-MM-DDTHH:mm')})

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    km = request.args.get('km', 999, type=float)
    begin = request.args.get("beginning", "now", type=str)
    distance = request.args.get("distance", 999, type=float)
    open_time = acp_times.open_time(km, distance, arrow.get(begin)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, distance, arrow.get(begin)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

@app.route("/submit", methods=['POST'])
def Submit():
    body = request.get_json()
    contents = {
        "start_time": body['Start'],
        "length": body['TotalDistance'],
        "checkpoints": body['Controls']
    }
    r = requests.post(f"http://api:{API_PORT}/api/Brevets", json=contents)
    print("status code ", r.status_code, flush=True)
    return flask.Response(status=r.status_code)


@app.route("/display")
def display():
    body = requests.get(f"http://api:{API_PORT}/api/Brevets").json()
    return flask.jsonify(brevets={"Start": body[-1]['start_time'], "Total": body[-1]['length'], "Controls": body[-1]['checkpoints']}, status=200)
#############

if __name__ == "__main__":
    print("Opening  for global access on port {}".format(BREVETS_PORT))
    app.run(port=BREVETS_PORT, host="0.0.0.0")
