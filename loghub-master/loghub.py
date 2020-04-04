from flask import Flask, request, json, abort, render_template
from redis import StrictRedis

app = Flask(__name__, static_url_path='')
redis = StrictRedis(host='localhost', port=6379, db=0)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/views/<log>', methods=['GET'])
def get_log_page(log):
    # try:
    if check_log_name(log):
        if redis.keys(log):
            data, last_entry = format_log_data(log)
            entry_count = redis.llen(log)
            return render_template('view.html', data=data, entry_count=entry_count, last_entry=last_entry, log_name=log)
        else:
            return abort(404)
    else:
        return abort(400)
        # except Exception as e:
        #    return abort(500)


@app.route('/logs/<log>', methods=['GET'])
def get_log_data(log):
    return log


@app.route('/logs/<log>/config', methods=['GET'])
def get_log_config(log):
    # try:
    if check_log_name(log):
        if redis.keys(log):
            data, last_entry = format_log_data(log)
            entry_count = redis.llen(log)
            return render_template('view.html', data=data, entry_count=entry_count, last_entry=last_entry, log_name=log)
        else:
            return abort(404)
    else:
        return abort(400)
        # except Exception as e:
        #    return abort(500)


@app.route('/logs/<log>', methods=['PUT'])
def add_log_data(log):
    if check_log_name(log) is not True or check_log_data(request.json['data']) is not True:
        return abort(400)
    else:
        try:
            redis.lpush(log, json.dumps({'datetime': request.json['datetime'], 'data': request.json['data']}))
            return ""
        except Exception as e:
            pass


@app.route('/logs', methods=['POST'])
def create_log():
    try:
        log_id = redis.incr('log_id')
        redis.hmset('log', {'id': log_id})
        response = app.response_class(response=json.dumps({'id': str(log_id)}), status=200, mimetype='application/json')
        return response
    except Exception as e:
        return str(e)


@app.route('/logs/<log>', methods=['DELETE'])
def delete_log(log):
    try:
        redis.delete(log)
        return ''
    except Exception as e:
        print(e)
        pass


def check_log_name(name):
    if len(name) <= 0:
        return False
    else:
        return True


def check_log_data(data):
    if not isinstance(data, float):
        return False
    else:
        return True


def format_log_data(log):
    data = redis.lrange(log, 0, -1)
    dict = {}
    x = []
    y = []
    last_entry = json.loads(data[-1])['datetime']
    for entry in data:
        entry = json.loads(entry)
        x.append(entry['datetime'])
        y.append(entry['data'])
    dict['x'] = x
    dict['y'] = y
    dict['type'] = 'scatter'
    return [dict], last_entry


if __name__ == '__main__':
    app.run(debug=True)
