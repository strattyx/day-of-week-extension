import json
import datetime
import time

from flask import Flask, render_template, request, url_for, jsonify

app = Flask(__name__)


# used for normal operation
@app.route('/invoke/realtime', methods=['POST'])
def realtime():
    # in this example we don't need to use arguments
    # if we did, we could do like this
    #body = request.get_json()
    #args = body['arguments']
    
    return datetime.datetime.today().weekday()


# used for backtests
@app.route('/invoke/timeline', methods=['POST'])
def timeline(): 
    body = request.get_json()
    ret = {}
    return ret

# 
if __name__ == '__main__':
    app.run(debug=True)
