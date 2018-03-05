#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import redis
from flask import Flask, render_template, send_file, redirect, request, url_for, make_response
from redisStore import redisDB

myRedis = redisDB()

app = Flask(__name__)

@app.route('/')
def mainpage():
    response = make_response(render_template('mainpage.html'))
    return response


@app.route('/query', methods=['POST'])
def query():

    global myRedis
    print "["+ __name__ + "] Log >> " + "Reading contents from Redis"
    content = myRedis.read_content()
    print "["+ __name__ + "] Log >> contents are:"
    print content
    response = make_response(render_template('results.html', **content))
    return response

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
