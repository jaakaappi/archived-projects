import discord
import os
import json
import models
import traceback

from sqlalchemy.orm import sessionmaker, exc
from datetime import datetime


def import_config():
    try:
        with open(os.path.join(os.getcwd(), 'config.json')) as file:
            return json.loads(file.read()), file
    except OSError as error:
        print('Error while opening config.json: {}'.format(error))
        print('Cannot continue without a working config file ;__;')
        exit()


config, file = import_config()  # todo check that all keywords are defined
client = discord.Client()


@client.event
async def on_message(message):
    if message.content == '!register':
        try:
            session = sessionmaker(bind=models.engine)()
            channel = models.Channel(id=message.channel.id, datetime_registered=datetime.now())
            session.add(channel)
            session.add(models.LogEntry(datetime=datetime.now(), channel=channel, message="Registered channel"))
            session.commit()
            await client.send_message(message.channel, 'This channel has been registered!')
        except:
            traceback.print_exc()
            await client.send_message(message.channel, 'There was an error on my side ;_; pwease try again later')
    if message.content == '!unregister':
        try:
            session = sessionmaker(bind=models.engine)()
            channel = session.query(models.Channel).filter_by(id=message.channel.id).one()
            session.delete(channel)
            session.add(models.LogEntry(datetime=datetime.now(), channel=channel, message="Unregistered channel"))
            session.commit()
            await client.send_message(message.channel, 'This channel has been unregistered! Sad to see you go ;_;')
        except exc.NoResultFound:
            await client.send_message(message.channel, 'Channel is not registered')
        except:
            traceback.print_exc()
            await client.send_message(message.channel, 'There was an error on my side ;_; pwease try again later')

if config['devmode']:
    print('--- Devmode active! ---')
    models.drop_and_create_all()

client.run(config['discord-token'])
