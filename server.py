from flask import Flask, request, jsonify
from gunicorn.app.base import BaseApplication
import multiprocessing
import sys
import os

app = Flask(__name__)

@app.route('/api')
def api():
    return jsonify({'hello_response': 'Hello to api route'})

@app.route('/api/test_params/<param_value>')
def testParams(param_value):
    return jsonify({
        'hello_response': 'Hello to api route', 
        'param_response': param_value
    })

@app.route('/api/test_query_params')
def testQueryPamans():
    param_value = request.args.get('param_value')
    return jsonify({
        'hello_response': 'Hello to query params route',
        'param_response': param_value
    })

@app.route('/api/test_header')
def testHeader():
    param_value = request.headers['param_value']
    return jsonify({
        'hello_response': 'Hello to header route',
        'param_response': param_value
    })

@app.route('/api/test_body')
def testBody():
    param_value = request.json['param_value']
    return jsonify({
        'hello_response': 'Hello to body route',
        'param_response': param_value
    })

class StartServer(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == '__main__':
    if('--prod' in sys.argv):
        options = {
            'bind': '%s:%s' % ('0.0.0.0', '8000'),
            'workers': (multiprocessing.cpu_count() * 2) + 1,
        }
        StartServer(app, options).run()
    else:
        os.environ['FLASK_ENV'] = "development"
        app.run()