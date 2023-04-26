import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

###############Load config.json and get path variables
def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

##############Function for reporting
import diagnostics
import sklearn.metrics

show_plot = False

def score_model():
    #calculate a confusion matrix using the test data and the deployed model
    #write the confusion matrix to the workspace
    df = diagnostics.load_csv_file(load_config()['test_data_path'], 'testdata.csv')
    pred = diagnostics.model_predictions(df)
    Y = df.iloc[:, -1].to_numpy()
    print(f'Predictions:\n{pred}')
    confusion_m = sklearn.metrics.confusion_matrix(Y, pred)
    tn, fp, fn, tp = confusion_m.ravel()
    print(f'tn={tn}, fp={fp}, fn={fn}, tp={tp}')
    #plot_confusion_matrix(y_true = Y, labels )
    disp = sklearn.metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_m, display_labels = ['0', '1']) #, display_labels = clf.classes_)
    disp.plot() 
    f = os.path.join(load_config()['output_model_path'], 'confusionmatrix.png')
    plt.savefig(f, format = 'png')
    print(f'Confusion matrix plot saved to the file "{f}".')
    if show_plot: plt.show()

if __name__ == '__main__':
    score_model()
