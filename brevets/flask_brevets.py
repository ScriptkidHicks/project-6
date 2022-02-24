"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import os
###
# Globals
###
app = flask.Flask(__name__)

###
# Environmental Variables
###

api_port = os.environ.get('API_PORT')

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
    status = insert(request)
    return flask.Response(status=status)


@app.route("/display")
def display():
    Start, Total, Controls = retreive()
    if (Controls == 404):
        return flask.jsonify(status=404, brevets={"Start": "", "Total": "", "Controls": ""})
    elif (Controls == 500):
        return flask.jsonify(status=500, brevets={"Start": "", "Total": "", "Controls": ""})
    return flask.jsonify(brevets={"Start": Start, "Total": Total, "Controls": Controls})
#############

if __name__ == "__main__":
    print("Opening  for global access on port {}".format(api_port))
    app.run(port=api_port, host="0.0.0.0")
