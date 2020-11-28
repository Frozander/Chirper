import os
import re
from gevent.pywsgi import WSGIServer  # Imports the WSGIServer
from gevent import monkey
monkey.patch_all()

from chirper import create_app

app = create_app()

if __name__ == "__main__":

    hostname = 'localhost.dev'
    port = 1337
    LISTEN = (hostname, port)

    key_rgx = re.compile(r'.*key.pem$')
    key_candidates = []
    for root, dirs, files in os.walk('ssl'):
        key_candidates = [os.path.join(root, x)
                          for x in files if key_rgx.match(x)]
    key = key_candidates[0] if key_candidates else 'key.pem'

    cert_rgx = re.compile(r'^(?=.*\.pem)(?:(?!.*key\.pem).)+$')
    cert_candidates = []
    for root, dirs, files in os.walk('ssl'):
        cert_candidates = [os.path.join(root, x)
                           for x in files if cert_rgx.match(x)]
    cert = cert_candidates[0] if cert_candidates else 'cert.pem'

    cert = cert.replace('\\', '/')
    key = key.replace('\\', '/')

    print(f'\nServing {app.name} at: https://{hostname}:{port}\n')

    http_server = WSGIServer(LISTEN, app,
                             keyfile=key,
                             certfile=cert)
    http_server.serve_forever()
