#coding: utf8
import os

SWARM_URL = os.getenv("SWARM_URL", "")

CA_PEM = os.getenv("CA_PEM", "")
CERT_PEM = os.getenv("CERT_PEM", "")
KEY_PEM = os.getenv("KEY_PEM", "")

JSON_HEADERS = {"Content-Type": "application/json"}

PROJECTS_API_PATH = 'projects/'
SERVICES_API_PATH = 'services/'

MAX_RETRY_TIMES = 3
