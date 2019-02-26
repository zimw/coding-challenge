from flask import Flask, request, abort
from redis import Redis, RedisError
import os
import socket
import json

from flask_json import FlaskJSON, JsonError, json_response, as_json
import hashlib

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)
FlaskJSON(app)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

@app.route('/replytime')
def get_time():
    now = datetime.utcnow()
    return json_response(time=now)

@app.route('/messages',methods=['POST'])
@as_json
def message():
    data = request.get_json(force=True)
    try:
        message = str(data['message'])
        print(message)
    except(KeyError, TypeError, ValueError):
        raise JsonError(description = 'Invalid message.')

    hm = hashlib.sha256(message.encode()).hexdigest()

    
    redis.hmset("DigestVsMessage",{hm:message})
    
    return dict(digest = hm)

@app.route('/messages/<path:subpath>')
@as_json
def message_subpath(subpath):
    if redis.hexists("DigestVsMessage", subpath):
        
        message = redis.hget("DigestVsMessage",subpath)
        
        return dict(message = message)
    else:
        abort(404)
        return dict(err_msg = 'Message not found')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

