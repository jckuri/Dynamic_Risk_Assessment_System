from flask import Flask, session, jsonify, request
import flask_restful
import pandas as pd
import numpy as np
import pickle
import diagnostics 
import json
import os

######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'
api = flask_restful.Api(app)

def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

#######################Prediction Endpoint
#@app.route("/prediction", methods=['POST','OPTIONS'])
#def predict():        
#    #call the prediction function you created in Step 3
#    return #add return value for prediction outputs

class Predictions(flask_restful.Resource):
    def post(self):
        json_data = request.get_json(force=True)
        location = json_data['location']
        #print(f'location={location}')
        df = pd.read_csv(location)
        pred = diagnostics.model_predictions(df)
        pred = [int(p) for p in pred]
        #print(f'pred={pred}, type(pred)={type(pred)}')
        json_dict = {'predictions': list(pred)}
        return json.dumps(json_dict)

api.add_resource(Predictions, '/prediction')

#######################Scoring Endpoint
import scoring

@app.route("/scoring", methods=['GET','OPTIONS'])
def scoring_endpoint():        
    #check the score of the deployed model
    f1_score = scoring.score_model()
    return {'f1_score': f1_score}
    #add return value (a single F1 score number)

######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats_endpoint():        
    #check means, medians, and modes for each column
    df = diagnostics.load_csv_file(load_config()['output_folder_path'], 'finaldata.csv')
    return diagnostics.dataframe_summary(df)
    #return a list of all calculated summary statistics

#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def diagnostics_endpoint():        
    #check timing and percent NA values
    times = diagnostics.execution_time()
    df = diagnostics.load_csv_file(load_config()['output_folder_path'], 'finaldata.csv')
    na_percentages = diagnostics.missing_data(df)
    outdated_packages = diagnostics.outdated_packages_list()
    return {'times': times, 'na_percentages': na_percentages, 'outdated_packages': outdated_packages}
    #add return value for all diagnostics

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
