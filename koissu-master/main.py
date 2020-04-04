import busio
import time
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA

ACTUATION_RANGE = 270

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)
pca.frequency = 50

# assign servo numbers to groups
servos = []
left_hips = [2, 6, 10]
right_hips = [0, 4, 8]
left_knees = [3, 7, 11]
right_knees = [1, 5, 9]

set1hips = [0, 6, 8]
set1knees = [1, 7, 9]
set2hips = [2, 4, 10]
set2knees = [3, 5, 11]

# list of commands:
commands = ['lefthips', 'righthips', 'leftknees', 'rightknees', 'run', 'sit', 'reset']


class MyServo:
    def __init__(self, channel):
        self.servo = servo.Servo(pca.channels[channel], actuation_range=ACTUATION_RANGE, max_pulse=2700)
        self.joint = 'hip' if i % 2 == 0 else 'knee'
        self.index = channel
        self.centerValue = 90
        self.upValue = 90
        self.downValue = 90

    def center(self):
        self.servo.angle = self.centerValue

    def up(self):
        self.servo.angle = self.upValue

    def down(self):
        self.servo.angle = self.downValue


for i in range(0, 12):
    servos.append(MyServo(i))

# center 150
# front 100
# back 220
for i in left_hips:
    servos[i].centerValue = 150
    servos[i].upValue = 210
    servos[i].downValue = 120

# center 170
# front 220
# back 100
for i in right_hips:
    servos[i].centerValue = 170
    servos[i].upValue = 120
    servos[i].downValue = 210

# up 100
# down 190
for i in left_knees:
    servos[i].centerValue = 150
    servos[i].upValue = 220
    servos[i].downValue = 100
# up 180
# down 110
for i in right_knees:
    servos[i].centerValue = 150
    servos[i].upValue = 110
    servos[i].downValue = 180


# commands for invidual controll:
def lefthips(angle):
    angle = int(angle)
    if angle < 0 or angle > ACTUATION_RANGE:
        print('Invalid angle')
        return
    for i in left_hips:
        servos[i].servo.angle = angle


def righthips(angle):
    angle = int(angle)
    if angle < 0 or angle > ACTUATION_RANGE:
        print('Invalid angle')
        return
    for i in right_hips:
        servos[i].servo.angle = angle


def leftknees(angle):
    angle = int(angle)
    if angle < 0 or angle > ACTUATION_RANGE:
        print('Invalid angle')
        return
    for i in left_knees:
        servos[i].servo.angle = angle


def rightknees(angle):
    angle = int(angle)
    if angle < 0 or angle > ACTUATION_RANGE:
        print('Invalid angle')
        return
    for i in right_knees:
        servos[i].servo.angle = angle


def sit():
    """
    Koissu sits
    """
    for i in left_hips + right_hips:
        servos[i].center()
    for i in left_knees + right_knees:
        servos[i].up()


def reset():
    i2c.unlock()


def run(strtimes):
    stay()
    """
    simple walking script
    :param times: string how many steps to take
    """
    times = int(strtimes)
    if times > 0:
        for j in range(times):
            for i in set1knees:
                servos[i].down()
            for i in set2knees:
                servos[i].up()
            time.sleep(0.5)

            for i in set1hips:
                servos[i].up()
            for i in set2hips:
                servos[i].down()
            time.sleep(0.5)

            for i in set2knees:
                servos[i].down()
            for i in set1knees:
                servos[i].up()
            time.sleep(0.5)

            for i in set2hips:
                servos[i].up()
            for i in set1hips:
                servos[i].down()
            time.sleep(0.5)
    else:
        for j in range(-times):
            for i in set1knees:
                servos[i].down()
            for i in set2knees:
                servos[i].up()
            time.sleep(0.5)
            for i in set1hips:
                servos[i].down()
            for i in set2hips:
                servos[i].up()
            time.sleep(0.5)
            for i in set2knees:
                servos[i].down()
            for i in set1knees:
                servos[i].up()
            time.sleep(0.5)
            for i in set2hips:
                servos[i].down()
            for i in set1hips:
                servos[i].up()
            time.sleep(0.5)
    lastStep(times)


def lastStep(direction):
    if direction > 0:
        for i in set1knees:
            servos[i].down()
        for i in set2knees:
            servos[i].up()
        time.sleep(0.5)
        for i in set1hips + set2hips:
            servos[i].center()
    else:
        for i in set1knees:
            servos[i].down()
        for i in set2knees:
            servos[i].up()
        time.sleep(0.5)
        for i in set1hips + set2hips:
            servos[i].center()
    time.sleep(0.5)
    sit()


def stay():
    for i in set1knees + set2knees:
        servos[i].down()
    time.sleep(0.8)


while True:
    try:
        command = input("Input command: ").split(' ')
        if command[0] not in commands:
            print("Command not in commands")
        elif len(command) == 2:
            locals()[command[0]](command[1])
        else:
            locals()[command[0]]()

    except KeyboardInterrupt:
        break

pca.deinit()
