# UOCIS322 - Project 6 #
Brevet time calculator with MongoDB, and a RESTful API!


## Overview

This is a brevet calculator with a mongodb database on the backend, designed to save your most recently submitted brevet, and retrieve it when desired. Submitting will clear the board of all currently entered control points. Additionally, if you attempt to submit an empty brevet, the frontend will give you a warning at the bottom, indicating that this is not the proper use of the calculator.


to submit a brevet you are wanting to store, simply use the `Submit` button, and to display the most recent brevet, use the `Display` button. 

### ACP controle times

This project consists of a web application that is based on RUSA's online calculator. The algorithm for calculating controle times is described here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here [https://rusa.org/pages/rulesForRiders](https://rusa.org/pages/rulesForRiders). The description is ambiguous, but the examples help. Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly. 

We are essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html). We can also use that calculator to clarify requirements and develop test data. 

### The logic of the calculator

If the distance is 0, then the opening time will be the opening time of the whole brevet, and the closing time will be an hour therafter. If the control is any other distance, then the total distance of that control will be divided by the relevant maximum and minimum speeds to provide the opening and closing times of that control. Note that while placing a control at 0 distance will result in a closing time an hour after the opening time of the race, any distance under 15km will not offer such a courtesy, and will result in a closing time before the closing time of the start of the race. It is advised that one does not do so, as a result.

## The API
	
	the  api 

## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.

Completed by Tammas Hicks
