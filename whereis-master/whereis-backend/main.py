from database import database
from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/locations', methods=['GET'])
def locations():
    return jsonify(database.get_locations())


@app.route('/items/<int:count>')
def items(count):
    return jsonify(database.get_items(count))


@app.route('/items', methods=['GET'])
def find_items():
    name = request.args.get('name')
    location = request.args.get('location')
    if name or location:
        items = database.get_items(None, name, location)
        return jsonify(items)
    else:
        return abort(400)


@app.route('/items', methods=['PUT', 'POST'])
def add_item():
    print(request.json)
    name = request.args.get('name')
    location = request.args.get('location')
    print('adding', name, location)
    return ""


if __name__ == '__main__':
    if database.is_empty():
        database.fill_test_db()
    app.run(host='0.0.0.0')
