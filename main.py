import json
import datetime
import time
from flask import Flask, render_template, request, url_for, jsonify
from pytz import timezone

'''
Day of week extension: 
- params:
	+ timezone:
		- unix timezone - "America/New_York"
'''

# day of week in timezone
def weekday(dt, tz):
	names = ['Monday', 'Tuesday', 'Wednesday', 
	'Thursday', 'Friday', 'Saturday', 'Sunday']

	if type(dt) == datetime.datetime:
		return names[dt.weekday()]

	try:
		# make datetime
		d = datetime.datetime.utcfromtimestamp(dt)
		# localize to desired tz
		d = timezone(tz).localize(d)
		# return appropriate day name
		return names[d.weekday()];
	except: 
		return names[datetime.datetime.utcfromtimestamp(dt).weekday()]


app = Flask(__name__)


# used for normal operation
@app.route('/invoke/realtime', methods = ['POST'])
def realtime():
	body = request.get_json()
	args = body['arguments']
	tz = args['Timezone']

	return json.dumps({ "return" : weekday(time.time(), tz) })

# used for backtests
@app.route('/invoke/timeline', methods = ['POST'])
def timeline(): 
	body = request.get_json()
	start, end = body['period']
	tz = body['arguments']['Timezone']

	print('Timeline request:', body)

	# convert from relative miliseconds to absolute timestamps
	now = int(time.time())
	start = start / 1000 + now
	end = end / 1000 + now

	# this is our timeline
	ret = {}

	def to_epoch(dt):
		return time.mktime(dt.timetuple())

	# start with weekday at start of period
	ret['start'] = { 'value' : weekday(start, tz) }
	
	# get local datetime
	dt = datetime.datetime.utcfromtimestamp(start)
	dt = timezone(tz).localize(dt)

	# truncate to date
	ts = to_epoch(dt.date())

	# add entry to update weekday each day
	while True:
		ts += 24 * 60 * 60 
		if ts < end:
			ret[int(ts * 1000 - now)] = { 'value' : weekday(ts, tz) }
		else:
			break

	return json.dumps({
		'timeline' : ret
	});

if __name__ == '__main__':
	app.run(port=5051)



