# Helper function to return a response with status code and CORS headers
import flask


def response(data, status_code):
    result = flask.jsonify(data)
    result.headers.set('Access-Control-Allow-Origin', '*')
    result.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT')
    return result, status_code