import redis
from gpiozero import LED
from time import sleep

r = redis.StrictRedis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('move')
led = LED(2)

while True:
    message = p.get_message()
    if message:
        led.on()
        sleep(5)
    led.off()
    sleep(1)
