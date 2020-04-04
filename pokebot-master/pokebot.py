import argparse
import arrow
import asyncio
import discord
import json
import os
import threading
import time
from redis import StrictRedis

redis = StrictRedis()
client = discord.Client()
helpfile = open('commandhelp', 'r')
helpstring = helpfile.read()
helpfile.close()
channels = []


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def channel_exists(channel_id):
    for ch in channels:
        if ch['id'] == channel_id:
            return True
    return False


def add_channel(channel):
    redis.lpush('channels', json.dumps(channel))


async def send_test_image(channel):
    directory = os.getcwd()

    with open(os.path.join(directory, 'images/001 Bulbasaur-0.png')) as f:
        await client.send_file(channel,
                               os.path.join(directory, 'images/001 Bulbasaur-0.png'),
                               content='{}, TJ {}'.format(os.path.basename(f.name)[4:-6].title(),
                                                          (arrow.get('14.06.2018',
                                                                     'DD.MM.YYYY') - arrow.now()).days + 1))


@client.event
async def on_message(message):
    # todo break into functions
    # todo support other batches
    if message.content.startswith('!'):
        if message.content.startswith('!aamuja'):
            parts = message.content.split(' ')
            channel = {}

            if len(parts) < 4:
                await client.send_message(message.channel, 'Komennosta puuttuu osia')
            else:
                try:
                    era = int(parts[1])
                    if era not in [1, 2]:
                        raise Exception()
                    channel['era'] = era
                except:
                    await client.send_message(message.server, 'Saapumiserän tulee olla 1 tai 2')
                    print('Virhe saapumiserässä: {} {} {}'.format(parts[1], message.channel, message.channel.name))
                    return
                try:
                    vuosi = int(parts[2])
                    if vuosi > 99 or vuosi < 0:
                        raise Exception()
                    channel['vuosi'] = vuosi
                except:
                    await client.send_message(message.channel, 'Vuoden tulee olla positiivinen kaksinumeroinen'
                                                               ' kokonaisluku')
                    print('Virhe vuodessa: {} {} {}'.format(parts[2], message.channel, message.channel.name))
                    return
                try:
                    kesto = int(parts[3])
                    if kesto not in [165, 255, 347]:
                        raise Exception()
                    channel['kesto'] = kesto
                except:
                    await client.send_message(message.channel, 'Keston tulee olla 165, 255 tai 347')
                    print('Virhe kestossa: {} {} {}'.format(parts[3], message.channel, message.channel.name))
                    return

                channel['id'] = message.channel.id

                # todo calculate next date

                print(channel)

                try:
                    if channel_exists(message.channel.id):
                        await client.send_message(message.channel, 'Kanava on jo rekisteröity')
                    else:
                        await client.send_message(message.channel, 'Kanava rekisteröity')
                        channels.append(channel)
                        print('Channel {} added'.format(message.channel.id))
                except Exception as e:
                    print(e)
                    await client.send_message(message.channel, 'Tietokantavirhe. Kehittäjälle on ilmoitettu')
                    # todo error logging

        elif message.content.startswith('!apua'):
            await client.send_message(message.channel, 'komennot:\n\n' + helpstring)
        elif message.content.startswith('!testimage'):
            await send_test_image(message.channel)
        elif message.content.startswith('!testcheck') and args.test is not None:
            await check_remaining_times()
        else:
            await client.send_message(message.channel, 'Tuntematon komento :<')
            # todo error logging


async def check_remaining_times(recurring=False):
    # todo support for other batches than 2/17 347
    # todo add error handling for missing channels

    now = arrow.now('Europe/Helsinki')
    next_time_seconds = now.replace(hour=6, minute=0, second=0).shift(days=+1).timestamp - now.timestamp

    if recurring:
        await asyncio.sleep(next_time_seconds)

    directory = os.getcwd()

    if not client.is_closed:

        print('Ran check, next check at {} after {} seconds'.format(now.shift(seconds=next_time_seconds),
                                                                    next_time_seconds))

        obsolete_channels = []

        for channel in channels:
            if client.get_channel(channel['id']) is not None:
                remaining_time = (arrow.get('14.06.2018', 'DD.MM.YYYY') - arrow.now()).days + 1
                if remaining_time < 151:
                    for f in os.listdir(os.path.join(directory, 'images/')):
                        if remaining_time == int(f.split('-')[0]):
                            with open(os.path.join(directory, 'images/' + f), 'r'):
                                await client.send_file(client.get_channel(channel['id']),
                                                       os.path.join(directory, 'images/' + f),
                                                       content='{}, TJ {}'.format(f.split('-')[1][:-4].title(),
                                                                                  remaining_time))
                            break
            else:
                obsolete_channels.append(channel)

        for channel in obsolete_channels:
            channels.remove(channel)
            print('Removed channel with ID ', channel['id'])


def restore_channels():
    print('Restoring channels')
    redischannels = redis.lrange('channels', 0, -1)
    for channel in redischannels:
        channel = json.loads(channel.decode('utf-8'))
        channels.append(channel)
    print('{} channels restored'.format(len(redischannels)))


parser = argparse.ArgumentParser()
parser.add_argument('--test', action='store_true')
parser.add_argument('--tokenfile', nargs=1)

args = parser.parse_args()

if args.tokenfile is None:
    tokenfile = open('token', 'r')
else:
    try:
        tokenfile = open(str(args.tokenfile[0]), 'r')
    except Exception as e:
        print('Error opening token file: ', e)
        exit()

token = tokenfile.read().strip()
print(token)
tokenfile.close()
if args.test is False:
    restore_channels()
else:
    print('In test mode, no channels restored')
client.loop.create_task(check_remaining_times(True))
client.run(token)

# todo move the whole shit to other branch, messages about releases based on release notes etc.
