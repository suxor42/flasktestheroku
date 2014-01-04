import os
from flask import Flask, jsonify
import datetime
try:
  from flask_cors import cross_origin # support local usage without installed package
except:
  from flask.ext.cors import cross_origin # this is how you would normally import

app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/time', methods=['GET'])
@cross_origin()
def printtime():
    return jsonify({'time':str(datetime.datetime.now())})

#@app.route('')

@app.route('/<parameter>')
def parameter_return(parameter):
    return parameter



#@app.route('/')

if __name__ == '__main__':
    app.run()
