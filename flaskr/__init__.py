#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "test"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

'''# Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = "grupo1"
POSTGRESUSER = "grupo1"
POSTGRESPASS = "grupo1"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)
'''

#Cambiar por Path Absoluto en el servidor
# QUERIES_FILENAME = 'var/www/FlaskDB/flaskr/queries'
QUERIES_FILENAME = 'queries'


@app.route("/", methods=['GET','POST'])
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo", methods=['GET','POST'])
def mongo():
    query = request.args.get("query")
    query = query.split("PARAMETER")
    print(query)
    try: #lo que debería pasar pero no pasa, porque form no tiene text, que está en file.html...
        param = request.form['text']
        query = param.join(query)
    except KeyError: #el caso pa que no falle
        print("YOLO")
        query = "2016-10-24".join(query)
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"


@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run(debug=True)
