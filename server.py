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
    return None

@APP.route("/logs",methods=["POST"])
def log_response():
    global STATS
    global RANGES
    global mutex
    logger.info(request.data)

    inputs = [x.split(b':') for x in request.data.split(b'\n')]
    for param in inputs:
        param[0] = param[0].decode('utf-8')
        if len(param[0]) > 2:
            if RANGES[param[0]](float(param[1])):
                STATS[param[0]][0] += float(param[1])
                STATS[param[0]][1] += 1
    print(STATS)
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
