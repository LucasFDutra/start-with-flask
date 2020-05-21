from flask import Flask, request, jsonify
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

os.environ['FLASK_ENV'] = 'development'
app.run()