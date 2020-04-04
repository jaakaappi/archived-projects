import aiohttp
import aiohttp_jinja2
import argparse
import jinja2
import os
from aiohttp import web
from datetime import datetime, timedelta
from models import Base, Data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

parser = argparse.ArgumentParser()
parser.add_argument('--mock', help='Use mock sensors', action='store_true')
args = parser.parse_args()

actions = []
websocket_subscriptions = []

if args.mock:
    sql_engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(sql_engine)
    Session = sessionmaker(bind=sql_engine)
    sql_session = Session()
    sql_session.query(Data).delete()
else:
    sql_engine = create_engine("sqlite:///production.db")
    Base.metadata.create_all(sql_engine)
    Session = sessionmaker(bind=sql_engine)
    sql_session = Session()


async def handle(request):
    response = aiohttp_jinja2.render_template('graph.html', request, create_context())
    return response


async def websocket_handler(request):
    # TODO fix reconnection, client does not receive updates despite of asking them. server receives requests for
    # updates
    ws = web.WebSocketResponse(heartbeat=10)
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'update':
                ws.send_json(create_context())

    return ws


async def post_handler(request):
    json_content = await request.json()
    if json_content["plant"] is None:
        return web.Response(status=400, text="Plant name cannot be empty")
    if not isinstance(json_content["plant"], str):
        return web.Response(status=400, text="Plant name should be a string")
    if json_content["value"] is None:
        return web.Response(status=400, text="Value cannot be empty")
    else:
        try:
            plant = json_content["plant"]
        except ValueError:
            return web.Response(status=400, text="Could not parse plant")
        try:
            value = float(json_content["value"])
        except ValueError:
            return web.Response(status=400, text="Could not parse value")
        else:
            sql_session.add(Data(plant, value, datetime.now()))
            return web.Response(status=200)


def create_context():
    model_data = get_data_from_db()
    if len(model_data) is not 0:
        model_data = calculate_daily_averages(model_data)
        model_data.sort(key=lambda x: x.plant_name)

    graphs = []
    timestamps = {model_data[0].plant_name: 'x0'}
    graph_timestamps = ['x{}'.format(0), model_data[0].timestamp.timestamp() * 1000]
    graph_data = [model_data[0].plant_name, model_data[0].value]
    last_plant_name = model_data[0].plant_name
    iterator = 0

    for entry in model_data:
        if entry.plant_name != last_plant_name:
            iterator += 1
            timestamps[entry.plant_name] = 'x{}'.format(iterator)
            graphs.append(graph_data)
            graphs.append(graph_timestamps)

            graph_timestamps = ['x{}'.format(iterator), entry.timestamp.timestamp() * 1000]
            graph_data = [entry.plant_name, entry.value]
            last_plant_name = entry.plant_name
        else:
            graph_timestamps.append(entry.timestamp.timestamp() * 1000)
            graph_data.append(entry.value)

    graphs.append(graph_data)
    graphs.append(graph_timestamps)
    context = {
        'xs': timestamps,
        'data': graphs,
        'date': datetime.now().strftime('%d.%m.%Y %H:%M')
    }
    return context


def get_data_from_db():
    query = sql_session.query(Data.plant_name, Data.timestamp, Data.value).filter(
        Data.timestamp > datetime.now() - timedelta(days=14), Data.timestamp <= datetime.now())
    return query.all()


def calculate_daily_averages(data):
    data.sort(key=lambda x: x.timestamp)

    plant = data[0].plant_name
    plant_values = []
    timestamp = data[0].timestamp

    new_data = []

    for entry in data:
        if entry.plant_name != plant or entry.timestamp.date() != timestamp.date():
            new_data.append(Data(plant, sum(plant_values) / len(plant_values), timestamp))
            plant = entry.plant_name
            plant_values = [entry.value]
            timestamp = entry.timestamp
        else:
            plant_values.append(entry.value)

    return new_data


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), 'templates')))
app.router.add_get('/', handle)
app.router.add_static('/static', os.path.join(os.getcwd(), 'static'))
app.router.add_get('/ws', websocket_handler)
app.router.add_post('/data', post_handler)
web.run_app(app)  # todo implement app runners, close websockets gracefully and implement reconnect
# https://docs.aiohttp.org/en/stable/web_advanced.html#aiohttp-web-app-runners
