import json
import datetime
import pytz
import dateutil
from flask import Flask, render_template, request, url_for, jsonify

'''
Day of week extension: 
- params:
  + timezone:
    - unix timezone - "America/New_York", "UTC", etc.
'''

def localize(dt, tz):
	return pytz.timezone(tz).localize(dt)

# day of week in timezone
def weekday(dt, tz):
	names = [ 'Monday', 'Tuesday', 'Wednesday', 
		  'Thursday', 'Friday', 'Saturday',
		  'Sunday' ]

	if type(dt) == datetime.datetime:
		return names[dt.weekday()]


app = Flask(__name__)


# used for normal operation
@app.route('/invoke/realtime', methods = ['POST'])
def realtime():
	body = request.get_json()
	args = body['arguments']
	tz = args['Timezone']
	now = datetime.datetime.today()
	return json.dumps({ 'return' : weekday(now, tz) })



# used for backtests
@app.route('/invoke/timeline', methods = ['POST'])
def timeline(): 
	body = request.get_json()
	start, end = body['period']
	tz = body['arguments']['Timezone']

	print('Timeline request:', body)

	# get period start and end points
	start = localize(dateutil.parser.parse(start), tz)
	end = localize(dateutil.parser.parse(end), tz)

	# value timeline
	ret = {}

	# initial value is weekday at start of period
	ret['start'] = { 'value' : weekday(start, tz) }

	# truncate to date
	dt = start.date()

	# add entry to update value at 0:00 daily
	while True:
		dt += datetime.timedelta(days = 1)
		if dt < end:
			ret[dt] = { 'value' : weekday(dt, tz) }
		else:
			break

	return json.dumps({
		'timeline' : ret
	});


	'''
	{ # initial value of monday gets updated daily
		'start' : 'Monday',
		'2001-1-1' : 'Tuesday',
		'2001-1-2' : 'Wednesday',
		...
	}
	'''


# start server
if __name__ == '__main__':
	app.run(port=5051)

