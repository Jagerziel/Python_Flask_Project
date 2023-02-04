# Imports
from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

# NOTE--START<<<BOILER PLATE FOR PEEWEE>>>
# Create database - specify db_name, user, password, host, and port
db = PostgresqlDatabase('people', user='postgres', password='12345',
    host='localhost', port=5432)


# Create base model to pull from database
class BaseModel(Model):
    class Meta:
        database = db

# Connect to DB
db.connect()

# NOTE--END <<<BOILER PLATE FOR PEEWEE>>>


class CovidCases(BaseModel):
    country_name = CharField()
    cases_total = IntegerField()
    deaths_total = IntegerField()
    population = IntegerField()
    # cases_total_1M_pop = GENERATED ALWAYS AS (cases_total / (population / 1000000)) STORED

# Drop current data and re-seed
db.drop_tables([CovidCases])
db.create_tables([CovidCases])

# Add data to CovidCases table
CovidCases(
    country_name="USA", 
    cases_total=104453003,
    deaths_total=1135957,
    population=334805269
    ).save()

CovidCases(
    country_name="USA", 
    cases_total=44683250,
    deaths_total=530745,
    population=1406631776
    ).save()




