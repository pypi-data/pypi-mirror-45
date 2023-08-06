import json
import requests
from .config import *
from .common import *

@auto_retry()
def send_get_request(path, params=None):
    require_path = SWARM_URL + path
    res = requests.get(require_path,
                    params=params,
                    verify=CA_PEM,
                    cert=(CERT_PEM, KEY_PEM))
    return res.status_code, json.loads(res.text)

@auto_retry()
def send_post_request(path, headers=None, params=None, data=None):
    require_path = SWARM_URL + path
    res = requests.post(require_path,
                        headers=headers,
                        params=params,
                        data=json.dumps(data),
                        verify=CA_PEM,
                        cert=(CERT_PEM, KEY_PEM))
    return res.status_code, json.loads(res.text)

@auto_retry()
def send_delete_request(path, headers=None, data=None):
    require_path = SWARM_URL + path
    res = requests.delete(require_path,
                        headers=headers,
                        data=json.dumps(data),
                        verify=CA_PEM,
                        cert=(CERT_PEM, KEY_PEM))
    return res.status_code, json.loads(res.text)
