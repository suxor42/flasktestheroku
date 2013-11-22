import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<parameter>')
def parameter_return(parameter):
    return parameter

#if __name__ == '__main__':
#    app.run()
