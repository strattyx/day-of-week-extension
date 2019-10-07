import json
import datetime
import time

from flask import Flask, render_template, request, url_for, jsonify

app = Flask(__name__)

def weekday(dt):
	names = ['Monday', 'Tuesday', 'Wednesday', 
			'Thursday', 'Friday', 'Saturday', 'Sunday']

	if type(dt) == datetime.datetime:
		return names[dt.weekday()]
	else:
		return names[datetime.datetime.fromtimestamp(dt).weekday()]


# used for normal operation
@app.route('/invoke/realtime', methods = ['POST'])
def realtime():
    # in this example we don't need to use arguments
    # if we did, we could do like this
    #body = request.get_json()
    #args = body['arguments']
    
    return weekday(time.time())


# used for backtests
@app.route('/invoke/timeline', methods = ['POST'])
def timeline(): 
    body = request.get_json()
    start, end = body['period']

	# convert from relative miliseconds to absolute timestamps
	now = int(time.time())
	start = start / 1000 + now
	end = end / 1000 + now

	# this is our timeline
	ret = {}

	def to_epoch(dt):
		return time.mktime(dt.timetuple())

	# start with weekday at start of period
	ret['start'] = { 'value' : weekday(start) }
	
	# truncate to day
	d = datetime.datetime.fromtimestamp(start).date()

	# add entry to update day of week in timeline
	while True:
		d += datetime.timedelta(days=1)
		ts = to_epoch(d)
		if ts < end:
			ret[ts] = { 'value' : weekday(d) }
		else:
			break

    return json.dumps({
    	'timeline' : ret
    });

if __name__ == '__main__':
    app.run(debug=True)
