from flask import Flask, request
from boto.dynamodb2.table import Table
import boto.swf.layer2 as swf
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
app = Flask(__name__)
file_handler = RotatingFileHandler('/var/log/postmash/application.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)
posts = Table('posts')


@app.route('/')
def butt():
    return 'Butt'

@app.route('/twoposts')
def twoposts():
    post1 = posts.get_item(postid='1')
    post2 = posts.get_item(postid='2')
    return json.dumps({'post1':dict(post1),'post2':dict(post2)})

@app.route('/postwinner', methods=['POST'])
def postwinner():
    data = request.json
    data.update({"timestamp":datetime.now().strftime(TIME_FORMAT)})
    swf.WorkflowType(name='PostMashWorkflow', domain='PostMashDomain',version='1.0', task_list='PostMashTasks').start(input=json.dumps(data))
    return '0', 200

if __name__ == '__main__':
    app.run()
