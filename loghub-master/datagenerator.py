import argparse
import datetime
import requests
import random


parser = argparse.ArgumentParser()
parser.add_argument('amount')
parser.add_argument('url')

args = parser.parse_args()
for i in range(0, int(args.amount)):
    print(requests.put(args.url,
                       json={'datetime': str(datetime.datetime.now() +
                                             datetime.timedelta(hours=i * 6)),
                             'data': random.randrange(0, 100)}))
