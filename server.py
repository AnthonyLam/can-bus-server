from flask import Flask, request, make_response, jsonify
from threading import Lock, Thread

APP = Flask(__name__)
logger = APP.logger

STATS = {
    'RPM': [0.0, 0],
    'COOLANT': [0.0, 0],
    'SPEED': [0.0, 0],
    'MAF': [0.0, 0],
    'THROTTLE': [0.0, 0]
}

RANGES = {
    'RPM': lambda x: x >0 and x < 16383.75,
    'COOLANT': lambda x: x > -40 and x < 215,
    'SPEED': lambda x: x >0 and x < 255,
    'MAF': lambda x: x>0 and x<655.35,
    'THROTTLE': lambda x: x>0 and x<100
}

mutex = Lock()

def worker(data):
    global STATS
    global RANGES
    global mutex
    stat = {
        'RPM': 0.0,
        'COOLANT': 0.0,
        'SPEED': 0.0,
        'MAF': 0.0,
        'THROTTLE': 0.0
    }

    inputs = [x.split(':') for x in data.split('\n')]
    for param,value in inputs:
        if RANGES[param](float(value)):
            stat[param][0] += float(value)
            stat[param][1] += 1

    mutex.acquire()
    STATS.update(stat)
    mutex.release()

@APP.route("/logs",methods=["POST"])
def log_response():
    data = str(request.data)
    logger.info(data)
    thread = Thread(target=worker,args=(data))
    thread.start()
    thread.run()

    res = {'Done':True}
    return make_response(jsonify(res))

@APP.route("/apiai",methods=["POST"])
def api_log():
    global STATS
    return make_response(jsonify(STATS))

if __name__ == '__main__':
    PORT = 8080

    APP.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )