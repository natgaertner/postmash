from flask import Flask
from boto.dynamodb2.table import Table
import json
import logging
from logging.handlers import RotatingFileHandler
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

if __name__ == '__main__':
    app.run()
