import sys
import logging

logging.basicConfig(level=logging.DEBUG, filename='/var/www/html/Any/logs/Any.log', format='%(asctime)s %(message)s')
sys.path.insert(0, '/var/www/html/Any')
sys.path.insert(0, '/var/www/html/Any/any-venv/lib/python3.9/site-packages')
from main import app as application
