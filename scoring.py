from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

#################Load config.json and get path variables
def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

#################Function for model scoring
import os.path
from joblib import dump, load
from sklearn.metrics import f1_score

def read_f1_score(path, filename):
    try:
        f = open(os.path.join(path, filename), 'r')
        lines = f.readlines()
        f.close()
        if len(lines) == 0: return 0.
        score_string = lines[0][:-1]
        return float(score_string)
    except:
        return 0.

def write_score(score, f):
    f = open(f, "w")
    f.write(f'{score}\n')
    f.close()
    print(f'F1-score {score} saved in file "{f.name}".')

def predict(csv_file):
    print(f'Test data loaded from file "{csv_file}".')
    df = pd.read_csv(csv_file)
    X = df.iloc[:, 1:-1].to_numpy()
    Y = df.iloc[:, -1].to_numpy()
    print(f'X={X}')
    print(f'Y={Y}')    
    model_file = os.path.join(load_config()['output_model_path'], 'trainedmodel.pkl')
    lrc = load(model_file)
    print(f'Model was loaded from file "{model_file}".')
    pred = lrc.predict(X)
    return X, Y, pred

def score_model():
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file
    csv_file = os.path.join(load_config()['test_data_path'], 'testdata.csv')
    X, Y, pred = predict(csv_file)
    
    # average{‘micro’, ‘macro’, ‘samples’,’weighted’, ‘binary’} or None, default=’binary’
    f1 = f1_score(Y, pred)
    #f1 = f1_score(Y, pred, average = 'weighted')
    #f1 = f1_score(Y, pred, average = 'macro')
    #f1 = f1_score(Y, pred, average = 'micro')
    print(f'f1 score: {f1}')
    score_file = os.path.join(load_config()['output_model_path'], 'latestscore.txt')
    write_score(f1, score_file)
    return f1
    
if __name__ == '__main__':
    f1_score = score_model()
