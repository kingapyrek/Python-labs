import logging
import time
import random
import sys
from multiprocessing import Process

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Car:
    def __init__(self, name):
        self.name = name
        self.speed = 0
        self.angle = 0
        self.fuel = 30
        self.weather_cond = ''
        self.type_road = ''
        self.max_speed = 120
        self.max_safe_speed = 120

    def check_fuel(self):
        if self.fuel <= 0:
            self.act(Event('out of fuel', 3))

    def start(self):
        self.speed_up(20)

    def speed_up(self, new_speed):
        if (self.speed + new_speed) > self.max_speed:
            logging.warning('{} You\'re speeding!'.format(self.name))
            self.speed += new_speed
            self.act(Event('police', 3))
        elif(self.speed + new_speed) > self.max_safe_speed:
            logging.warning('{} It is not safe to '
                            'speed up more!'.format(self.name))
            self.act(Event('crash', 3))
        else:
            self.speed += new_speed
            self.fuel -= 2
            logging.info('{} Speeding up...'.format(self.name))
            time.sleep(1)
        self.check_fuel()

    def slow_down(self, new_speed):
        if (self.speed - new_speed) < 0:
            logging.info('{} Sorry, you cannot '
                         'slow down that much!'.format(self.name))
        else:
            self.speed -= new_speed
            self.fuel -= 1
            logging.info('{} Slowing down...'.format(self.name))
            time.sleep(1)
        self.check_fuel()

    def turn_right(self, new_angle):
        if self.speed > 25:
            self.slow_down(self.speed - 25)
        x = self.angle + new_angle
        if x > 360:
            self.angle = x - 360
        else:
            self.angle += new_angle
        self.fuel -= 1
        for _ in range(3):
            logging.info('{} Turning right ({} degrees)'
                         '...'.format(self.name, new_angle))
            time.sleep(0.5)
        self.check_fuel()

    def turn_left(self, new_angle):
        if self.speed > 25:
            self.slow_down(self.speed - 25)
        x = self.angle - new_angle
        if x < 0:
            self.angle = 360 + x
        else:
            self.angle -= new_angle
        self.fuel -= 1
        for _ in range(3):
            logging.info('{} Turning left ({} degrees)'
                         '...'.format(self.name, new_angle))
            time.sleep(0.5)
        self.check_fuel()

    def act(self, event):
        logging.info('{} An event\'s {} just happened! It\'ll last {} '
                     'seconds'.format(self.name, event.name, event.duration))
        self.fuel -= 1
        if event.name == 'crash':
            logging.info('{} Oops your car crashed '
                         'end of driving'.format(self.name))
            self.speed = 0
            raise KeyboardInterrupt

        if event.name == 'out of fuel':
            logging.warning('{} You ran out of fuel, '
                            'fueling up...'.format(self.name))
            self.fuel = 30

        for _ in range(event.duration):
            self.slow_down(int(self.speed / event.duration))

        if event.name == 'police':
            logging.warning('{} You are stopped by police'.format(self.name))
            if self.speed >= self.max_speed:
                logging.warning('{} You\'ve been fined for '
                                'speeding!'.format(self.name))
            else:
                logging.info('{} You\'re free to go!'.format(self.name))
        if event.name == 'crossroads':
            turn = random.choice(['turn_left', 'turn_right'])
            ev = 'self.' + turn
            eval(ev)(90)

        self.speed_up(15)
        self.check_fuel()


class Event:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration


class Environment:
    def __init__(self, car):
        weather = {'snowy': 1 / 3, 'fuggy': 1 / 4, 'sunny': 0, 'rainy': 1 / 4}
        road = {'highway': 120, 'country road': 30,
                'urban area': 50, 'open area': 90}
        car.type_road, car.max_speed = random.choice(list(road.items()))
        car.weather_cond, speed_decrease = random.choice(list(weather.items()))
        car.max_safe_speed = car.max_speed
        car.max_safe_speed -= car.max_safe_speed*speed_decrease
        logging.info('{} Today is {} weather and we\'re driving on {}.\n'
                     'Max speed permissible speed is {} and max safe speed '
                     'in those conditions is '
                     '{}.'.format(car.name, car.weather_cond,
                     car.type_road, car.max_speed, car.max_safe_speed))


methods = ['speed_up'] * 15 + ['slow_down'] * 25 + ['turn_left'] * 15\
        + ['turn_right'] * 15 + ['act'] * 30
Events = ['zebra crossing'] * 20 + ['traffic lights'] * 20\
       + ['obstacle'] * 20 + ['crash'] * 5 + ['traffic jam'] * 10\
       + ['police'] * 15 + ['crossroads'] * 10


def generator(car):
    while True:
        method = 'car.' + random.choice(methods)
        if method in ('car.speed_up', 'car.slow_down'):
            random_speed = random.randint(1, 50)
            yield eval(method)(random_speed)
        elif method in ('car.turn_left', 'car.turn_right'):
            random_angle = random.randint(1, 360)
            yield eval(method)(random_angle)
        elif method == 'car.act':
            event = random.choice(Events)
            random_dur = random.randint(1, 5)
            yield eval(method)(Event(event, random_dur))


def f(c):
    gen = generator(c)
    try:
        while True:
            next(gen)
            logging.info('{} current speed: {} and angle: '
                         '{}'.format(c.name, int(c.speed), c.angle))
    except KeyboardInterrupt:
        logging.info('{} End of simulation'.format(c.name))


if __name__ == "__main__":
    logging.info('To stop the simulation press Ctrl+C')
    c1 = Car('FORD')
    env = Environment(c1)
    c1.start()

    c2 = Car('CITROEN')
    env = Environment(c2)
    c2.start()

    p1 = Process(target=f, args=(c1,))
    p2 = Process(target=f, args=(c2,))
    try:
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        p1.terminate()
        p2.terminate()
