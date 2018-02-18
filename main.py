from flask import Flask, request
from datetime import datetime
import subprocess
import sys
import os
import argparse


app = Flask(__name__)
polyglot = ""


@app.route("/<service>/<method>", methods=['POST'])
def polyglot(service, method):
    root = request.headers.get('x-polyman-root')
    endpoint = request.headers.get('x-polyman-endpoint')
    root_flag = '--proto_discovery_root=' + os.path.expanduser(root)
    endpoint_flag = '--endpoint=' + endpoint
    method_flag = '--full_method='+service+'/'+method
    command_flag = '--command=call'
    start_time = datetime.now()
    echo = subprocess.Popen(["echo", request.data], stdout=subprocess.PIPE)
    poly = subprocess.Popen(['java', '-jar', polyglot, command_flag,
                            endpoint_flag, method_flag, root_flag,
                            '--use_reflection=true'],
                            stdin=echo.stdout, stdout=subprocess.PIPE)
    output = poly.communicate()[0]
    print(datetime.now() - start_time)
    return output


@app.route("/list_services", methods=['GET'])
def list():
    command_flag = '--command=list_services'
    root = request.headers.get('x-polyman-root')
    root_flag = '--proto_discovery_root=' + os.path.expanduser(root)

    poly_args = ['java', '-jar', polyglot, command_flag, root_flag]
    poly = subprocess.Popen(poly_args, stdout=subprocess.PIPE)
    output = poly.communicate()[0]
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--polyglot', default="~/polyglot.jar",
                        type=str, help="override to polyglot jar")
    args = parser.parse_args()
    polyglot = os.path.expanduser(args.polyglot)
    if not os.path.exists(polyglot):
        sys.exit("polyglot.jar does not exist")
    app.run(host='0.0.0.0', port=8082)
