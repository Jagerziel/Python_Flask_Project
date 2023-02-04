# Imports
from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

# NOTE--START<<<BOILER PLATE FOR PEEWEE>>>
# Create database - specify db_name, user, password, host, and port
db = PostgresqlDatabase('people', user='postgres', password='12345',
    host='localhost', port=12345)


# Create base model to pull from database
class BaseModel(Model):
    class Meta:
        database = db

# Connect to DB
db.connect()

# NOTE--END <<<BOILER PLATE FOR PEEWEE>>>

# Create Covid Cases Table
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


# Creating a flask server
app = Flask(__name__)

# Define routes
@app.route('/covid-cases/', methods=['GET', 'POST'])
@app.route('/covid-cases/<id>', methods=['GET', 'PUT', 'DELETE'])

# Functions for CRUD at endpoints
def endpoint(id=None):
    # GET Request
    if request.method == 'GET':
        # Take model, translate into covid-cases and model it to a dictionary
        if id:
            return jsonify(model_to_dict(CovidCases.get(CovidCases.id == id)))
        # Goes through person table and appends to list
        else:
            covid_list = []
            for covid_cases in CovidCases.select():
                covid_list.append(model_to_dict(covid_cases))
            return jsonify(covid_list)
    # PUT Request
    if request.method =='PUT':
        # Create variable to store json data
        body = request.get_json()
        # Use variable body to overwrite item at that id
        CovidCases.update(body).where(CovidCases.id == id).execute()
        return f"Covid Cases {str(id)} has been updated."
    # POST Request
    if request.method == 'POST':
        # Creates New Item and assigns it to variable
        new_country = dict_to_model(CovidCases, request.get_json())
        # Saves New Item
        new_country.save()
        return jsonify({"success": True})
    # DELETE Request
    if request.method == 'DELETE':
        # Delete where item is equal to id
        CovidCases.delete().where(CovidCases.id == id).execute()
        return f"Covid Cases entry at id {str(id)} has been deleted."

app.run(debug=True, port=54321)



