import os


DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = '111111'
DB_HOST = '127.0.0.1'
DB_PORT = 5432

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 55555

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_FILE = os.path.join(BASE_DIR, 'templates')