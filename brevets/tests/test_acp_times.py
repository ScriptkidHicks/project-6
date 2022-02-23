"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

from distutils.log import error
from genericpath import exists
import arrow
import nose    # Testing framework
from acp_times import open_time, close_time
import logging
from pymongo_methods import insert, retreive

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_zero_distance_open():
    inputTime = arrow.get("2022-02-03T20:27")
    outputTime = arrow.get("2022-02-03T20:27")
    assert outputTime == open_time(0, 1000, inputTime)

def test_negative_distance_open():
    inputTime = arrow.get("2022-02-03T20:27")
    outputTime = arrow.get("2022-02-03T20:27")
    assert outputTime == open_time(-100, 1000, inputTime)

def test_negative_total_distance_open_time():
    inputTime = arrow.get("2022-02-03T20:27")
    try:
        temp = open_time(100, -20, inputTime)
    except:
        print("passing a negative distance for the total failed")

def test_too_long_total_distance_open_time():
    inputTime = arrow.get("2022-02-03T20:27")
    brevetDistance = 200
    # the max brevet distance should be 240
    assert open_time(1000, brevetDistance, inputTime) == open_time(240, brevetDistance, inputTime)

def test_zero_distance_close_200():
    inputTime = arrow.get("2022-02-03T20:27")
    outputTime = inputTime.shift(hours=+1)
    assert outputTime == close_time(0, 200, inputTime)

def test_too_long_total_distance_close_time():
    inputTime = arrow.get("2022-02-03T20:27")
    assert close_time(1000, 200, inputTime) == close_time(240, 200, inputTime)

def test_submit_failure_norequest():
    temp1 = insert(None)
    assert(temp1 == 403)

def test_insert_and_retreive():
    # we manufacture our own request object for this
    class ourRequest:

        def __init__(self, Start, Total, Controls) -> None:
            self.form = {'Start': Start, 'TotalDistance': Total, 'Controls': Controls}

    #we don't really need to worry about formatting, which is taken care of the front end. We just need to worry about correctly subitting and retrieving latest
    tempRequest = ourRequest('01:32', '800km', 'the earlier control')
    insert(tempRequest)
    tempRequest = ourRequest("12:13", "100km", "Controls Series")
    insert(tempRequest)
    tempPull = retreive()
    assert tempPull == ('12:13', "100km", "Controls Series")