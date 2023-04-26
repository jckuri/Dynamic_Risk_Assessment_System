from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

##################Load config.json and correct path variable
def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

####################function for deployment
import shutil
import os.path

def copy_file(origin_path, origin_file, destiny_path):
    origin = os.path.join(origin_path, origin_file)
    destiny = os.path.join(destiny_path, origin_file)
    shutil.copyfile(origin, destiny) 
    print(f'File "{origin}" was successfully copied to "{destiny_path}".')

def store_model_into_pickle(model):
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    copy_file(model, 'trainedmodel.pkl', load_config()['prod_deployment_path'])
    copy_file(model, 'latestscore.txt', load_config()['prod_deployment_path'])
    copy_file(load_config()['output_folder_path'], 'ingestedfiles.txt', load_config()['prod_deployment_path'])
    
if __name__ == '__main__':
    store_model_into_pickle(load_config()['output_model_path'])
