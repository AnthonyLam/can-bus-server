from flask import Flask, request, make_response, jsonify

APP = Flask(__name__)
logger = APP.logger

@APP.route("/logs",methods=["POST"])
def log_response():
    logger.info(request.data)
    res = {'Done':True}
    return make_response(jsonify(res))

if __name__ == '__main__':
    PORT = 8080

    APP.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )