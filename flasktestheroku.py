import os
from flask import Flask, jsonify
import datetime
from flask.ext.cors import cross_origin
from flask.ext.redis import Redis

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost'
redis = Redis(app)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/time', methods=['GET'])
@cross_origin()
def printtime():
    return jsonify({'time': str(datetime.datetime.now())})

#@app.route('')

@app.route('/redis', methods=['GET'])
def redisinfo():
    info = redis.info()
    return info
    pass

@app.route('/<parameter>')
def parameter_return(parameter):
    return parameter



#@app.route('/')

if __name__ == '__main__':
    app.run()
