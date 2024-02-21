from itertools import product
from bson.objectid import ObjectId
import subprocess

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongo_config import db
import flask
import json
from bson import json_util


class Phenomizer(Resource):
    def post(self):
        postedData = request.get_json()
        print(postedData)
        hpo_terms = ",".join(obj.get("id") for obj in postedData)

        print(hpo_terms)

        command = f"java -jar phenomiser-cli-0.1.1.jar query -hpo hp.obo -da phenotype.hpoa -query {hpo_terms}"

        # Execute the Phenomiser command
        output = subprocess.check_output(
            command, shell=True, text=True, stderr=subprocess.STDOUT
        )
        print(output)

        # Split the output to retrieve the relevant data
        lines = output.split("out path not found. writing to console:")
        data = []
        if len(lines) > 1:
            # Split the data into lines and remove leading/trailing spaces
            lines = lines[1].strip().split("\n")

            # Split the header line into column names
            columns = [col.strip() for col in lines[0].split("\t")]

            # Create a list of dictionaries with column names as keys
            for line in lines[1:]:
                values = line.split("\t")
                data_dict = {}
                for i, col in enumerate(columns):
                    data_dict[col] = values[i].strip()
                data.append(data_dict)

        retJson = {
            "status": 200,
            "msg": " Succes complete diagnosis ",
            "data": data,
        }
        return jsonify(retJson)
