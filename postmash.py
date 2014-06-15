from flask import Flask, request, session, render_template
import json
import logging
import redis
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from rq import Queue
from postworker import enqueue_work
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False
#rsessions = redis.StrictRedis(host='localhost', port=6379, db=1)
#app.session_interface = RedisSessionInterface(rsessions)
file_handler = RotatingFileHandler('/var/log/postmash/application.log')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
q = Queue(connection=redis.StrictRedis(host='localhost',port=6379,db=1))
app.secret_key = os.getenv('SESSION_SECRET')

@app.route('/')
def butt():
    return render_template('index.html')

@app.route('/twoposts')
def twoposts():
    key1 = r.randomkey()
    key2 = r.randomkey()
    while key1 == key2:
	key2 = r.randomkey()
    post1 = r.get(key1)
    post2 = r.get(key2)
    app.logger.warn(session.modified)
    session['leftkey'] = key1
    session['rightkey'] = key2
    app.logger.warn(key1)
    app.logger.warn(key2)
    return json.dumps({'leftpost':{'postid':key1,'text':post1},'rightpost':{'postid':key2,'text':post2}})

@app.route('/mash', methods=['POST'])
def mash():
    data = dict(request.json)
    data.update({"timestamp":datetime.now().strftime(TIME_FORMAT), "remote_addr":request.remote_addr, "rightid":session['rightkey'],"leftid":session['leftkey']})
    session.clear()
    try:
	q.enqueue(enqueue_work, json.dumps(data))
    except Exception as e:
	app.logger.exception(e)
    return '0', 200

if __name__ == '__main__':
    app.run()
