import redis
import time
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app)

CONTROL_DURATION = 5

queue = []
control_start_time = 0

redis_queue = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('request_control')
def handle_control_event():
    if len(queue) == 0:
        queue.append(request.sid)
    if queue[0] == request.sid:
        json = {
            'status': 'control'
        }
        emit('status', json)
    else:
        place = len(queue)
        queue.append(request.sid)
        json = {
            'status': 'queued',
            'place': place
        }
        emit('status', json)


@socketio.on('disconnect')
def handle_disconnected():
    print(str(request.sid)+' disconnected')
    if request.sid in queue:
        queue.remove(request.sid)
        for client in queue:
            index = queue.index(client)
            json = {
                'place': index
            }
            send(json, room=client)


@socketio.on('move')
def handle_move_event(json):
    print('received json: ' + str(json))
    channel = redis_queue.pubsub()
    redis_queue.publish("move", json)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
