from flask import request, jsonify
from flask_lambda2 import FlaskLambda

app = FlaskLambda(__name__)


@app.route('/kits', methods=['POST'])
def kits_post():
    files = request.files.getlist('files')
    for file in files:
        print(file)
    print(request.form['title'])
    print(request.form['description'])
    print(request.form['kitType'])
    # print(values)
    return jsonify("success"), 201
