import json
import datetime
import pytz
import dateutil.parser
from flask import Flask, render_template, request, url_for, jsonify

'''
Day of week extension: 
- params:
  + timezone:
    - unix timezone - "America/New_York", "UTC", etc.
'''

# set timezone
def localize(dt, tz):
	return dt.astimezone(pytz.timezone(tz))

# day of week in timezone
def weekday(dt):
	names = [ 'Monday', 'Tuesday', 'Wednesday', 
		  'Thursday', 'Friday', 'Saturday',
		  'Sunday' ]
	return names[dt.weekday()]


app = Flask(__name__)


# used for normal operation
@app.route('/invoke/realtime', methods = ['POST'])
def realtime():
	body = request.get_json()
	tz   = body['arguments']['Timezone']
	now  = datetime.datetime.now()
	ret  = weekday(localize(now, tz))
	return json.dumps({ 'return' : ret })



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
	ret['start'] = { 'value' : weekday(start) }

	# truncate to date
	dt = start.date()

	# add entry to update value at 0:00 daily
	while True:
		dt += datetime.timedelta(days = 1)
		if dt < end:
			ret[dt] = { 'value' : weekday(dt) }
		else:
			break


	return json.dumps({
		'timeline' : ret, 	# value history
		'warn' : [],		# warnings for user to see
		'resolutions' : [],	# why things happened
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

