import os
from flask import Flask, request, json
import datetime
from flask.ext.cors import cross_origin
from flask.ext.redis import Redis

app = Flask(__name__)
app.config['REDIS_URL'] = os.environ['REDIS_URL']
redis = Redis(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/time', methods=['GET'])
@cross_origin()
def printtime():
    return json.dumps({'time': datetime.datetime.now()})


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

@app.route('/redis/lastrequests', methods=['GET'])
def lastsharedtrackingrequests():
    try:
        return json.dumps(map(json.loads, redis.lrange('requests', 0, -1)))
    except Exception, e:
        return str(e)

@app.route('/lastsales', methods=['GET'])
def lastsales():
    try:
        transactions = map(json.loads, redis.lrange('requests', 0, -1))
        sales = filter(lambda x: x['tracking-type'] == 'sale', transactions)
        #return str(sales)
        timeformat = '%a, %d %b %Y %H:%M:%S %Z'
        geckoitems = map(lambda x: (datetime.datetime.strptime(x['time'], timeformat) - datetime.datetime.strptime(x['tracking-time']).seconds, timeformat), sales)
        axisxmin = min(sales, key=lambda x: x['time'])
        axisxmax = max(sales, key=lambda x: x['time'])
        axisymin = min(geckoitems)
        axisymax = max(geckoitems)
        geckodata = {'items': geckoitems,
                     'settings': {
                         'axisx': [axisxmin,axisxmax],
                         'axisy': [axisymin,axisymax],
                     },
                     }
        return json.dumps(geckodata)
    except Exception, e:
        return str(e)



@app.route('/redis/<parameter>', methods=['GET'])
def getdata(parameter):
    return json.dumps({parameter: redis.get(parameter)})


@app.route('/redis/flush', methods=['GET'])
def flush():
    redis.flushdb()
    return 'done'


@app.route('/sharedtracking', methods=['GET'])
def storetrackingdata():
    try:
        tid = request.args.get('tid')
        referrer = request.remote_addr
        route = request.access_route
        trackingtime = datetime.datetime.strptime(request.args.get('ttime'), '%Y%m%dT%H%M%S%fZ')
        trackingtype = str(request.args.get('ttype'))
        #redis.set(tid, str(datetime.datetime.now()))
        dataobject = {'time': datetime.datetime.now(),
                      'tracking-time': trackingtime,
                      'tracking-id': tid,
                      'remote_addr': referrer,
                      'tracking-type': trackingtype,
                      'route': route,
        }
        redis.lpush('requests', json.dumps(dataobject))
        redis.ltrim('requests', 0, 99)
        redis.set('lastrequest', json.dumps(dataobject))
        return ''
    except Exception, e:
        return e


@app.route('/<parameter>')
def parameter_return(parameter):
    return parameter


if __name__ == '__main__':
    app.run()
