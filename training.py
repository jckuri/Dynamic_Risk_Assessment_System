from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json

###################Load config.json and get path variables
def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

#################Function for training the model
#from os.path import isfile, join
import os.path
from joblib import dump, load

def read_csv(f):
    return pd.read_csv(f)

def train_model():

    #use this logistic regression for training
    lrc = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True, intercept_scaling=1, l1_ratio=None, max_iter=100, multi_class='auto', n_jobs=None, penalty='l2', random_state=0, solver='liblinear', tol=0.0001, verbose=0, warm_start=False)
    
    #fit the logistic regression to your data
    csv_file = os.path.join(load_config()['output_folder_path'], 'finaldata.csv')
    print(f'csv_file={csv_file}')
    df = read_csv(csv_file)
    X = df.iloc[:, 1:-1].to_numpy()
    Y = df.iloc[:, -1].to_numpy()
    print(f'X={X}')
    print(f'Y={Y}')
    lrc.fit(X, Y)
    
    #write the trained model to your workspace in a file called trainedmodel.pkl
    model_file = os.path.join(load_config()['output_model_path'], 'trainedmodel.pkl')
    dump(lrc, model_file) 
    print(f'Model was saved in the file "{model_file}".')

if __name__ == '__main__':
    train_model()
