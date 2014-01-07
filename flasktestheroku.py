import os
from flask import Flask, jsonify, request, json
import datetime
from flask.ext.cors import cross_origin
from flask.ext.redis import Redis

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://redistogo:57de250887d0ed3fcc9e5f8262a5d312@albacore.redistogo.com:10078/'
redis = Redis(app)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/time', methods=['GET'])
@cross_origin()
def printtime():
    return json.dumps({'time': datetime.datetime.now()})

#@app.route('')


@app.route('/redis/info', methods=['GET'])
def redisinfo():
    info = redis.info()
    return json.dumps(info)
    pass


@app.route('/redis/keys', methods=['GET'])
def listkeys():
    try:
        result = json.dumps(redis.keys('*'))
    except Exception, e:
        result = str(e)
    return result

@app.route('/redis/last', methods=['GET'])
def lastsharedtrackingrequest():
    return redis.get('lastrequest')

@app.route('/redis/<parameter>', methods=['GET'])
def getdata(parameter):
    return json.dumps({parameter: redis.get(parameter)})


@app.route('/sharedtracking', methods=['GET'])
def storetrackingdata():
    tid = request.args.get('tid')
    trackingtime = datetime.datetime.strptime(request.args.get('ttime'),'%Y%m%dT%H%M%S%fZ')
    redis.set(tid, str(datetime.datetime.now()))
    redis.set('lastrequest', json.dumps({'time':datetime.datetime.now(), 'tracking-time': trackingtime, 'tracking-id': tid}))
    return
    pass


@app.route('/<parameter>')
def parameter_return(parameter):
    return parameter



#@app.route('/')

if __name__ == '__main__':
    app.run()
