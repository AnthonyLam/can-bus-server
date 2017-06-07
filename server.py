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

def get_avg(key):
    global STATS
    return int(STATS[key][0]/STATS[key][1])

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
    req = request.get_json(silent=True,force=True)
    action = req.get('result').get('action')
    logger.info(action)
    res = {
        'speech': None,
        'contextOut': req['result']['contexts']
    }


    if action == 'rpm':
        res['speech'] = "Your average RPM is {} rotations per minute".format(get_avg('RPM'))
    elif action == 'throttle':
        res['speech'] = "Your average throttle use was {} percent".format(get_avg("THROTTLE"))
    elif action == 'coolant':
        res['speech'] = "Your coolant was about {} degrees celsius on average".format(get_avg("COOLANT"))    
    elif action == 'maf':
        res['speech'] = "Your average air flow rate was {} grams per second".format(get_avg("MAF"))
    elif action == 'speed':
        res['speech'] = "Your average speed was {} kilometers per hour".format(get_avg("SPEED"))

    return make_response(jsonify(res))

if __name__ == '__main__':
    PORT = 8080

    APP.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )
