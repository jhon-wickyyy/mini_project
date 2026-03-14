import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data')
TEMPLATE_FILE = os.path.join(BASE_DIR, 'templates')
HOST = '127.0.0.1'
PORT = 55555