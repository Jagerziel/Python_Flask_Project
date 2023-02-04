# NOTE--START<<<BOILER PLATE FOR PEEWEE>>>
# Import peewee
from peewee import *

# Create database - specify db_name, user, password, host, and port
db = PostgresqlDatabase('people', user='postgres', password='12345',
    host='localhost', port=5432)

# Connect to DB
db.connect()