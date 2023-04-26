import json
import pandas as pd
import numpy as np
import timeit
import os

##################Load config.json and get environment variables
def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

##################Function to get model predictions
from joblib import dump, load

def model_predictions(df):
    #read the deployed model and a test dataset, calculate predictions
    X = df.iloc[:, 1:-1].to_numpy()
    Y = df.iloc[:, -1].to_numpy()
    print(f'X={X}')
    print(f'Y={Y}')    
    model_file = os.path.join(load_config()['prod_deployment_path'], 'trainedmodel.pkl')
    lrc = load(model_file)
    pred = lrc.predict(X)
    return list(pred) #return value should be a list containing all predictions
    
def test_predictions():
    df = load_csv_file(load_config()['test_data_path'], 'testdata.csv')
    pred = model_predictions(df)
    print(f'Predictions:\n{pred}')

##################Function to get summary statistics
def load_csv_file(folder_path, csv_file):
    csv_file = os.path.join(folder_path, csv_file)
    df = pd.read_csv(csv_file)
    print(f'Test data loaded from file "{csv_file}".')
    return df

def column_summary(name, values):
    if type(values[0]) == type('s'): return None
    mean = values.mean()
    median = np.median(values)
    stdev = values.std()
    return {'mean': mean, 'median': median, 'stdev': stdev}

def dataframe_summary(df):
    n_columns = df.shape[1]
    summary = {}
    for j in range(n_columns):
        column = df.iloc[:, j]
        stats = column_summary(column.name, column.to_numpy())
        if stats is None: continue
        summary[column.name] = stats
    return summary #return value should be a list containing all summary statistics
    
def test_dataframe_summary():
    df = load_csv_file(load_config()['output_folder_path'], 'finaldata.csv')
    summary = dataframe_summary(df)
    print(f'dataframe_summary:\n{df}')
    for column_name in summary:
        column = summary[column_name]
        print(f'column={column_name}, mean={column["mean"]}, median={column["median"]}, stdev={column["stdev"]}')
        
################## missing data

def missing_data(df):
    n_rows, n_columns = df.shape[0], df.shape[1]
    summary = {}
    percentages = []
    for j in range(n_columns):
        column = df.iloc[:, j]
        count = column.isna().sum()
        percent = count / n_rows
        percentages.append(percent)
    return percentages

def test_missing_data():
    df = load_csv_file(load_config()['output_folder_path'], 'finaldata.csv')
    print(f'missing_data:\n{df}')
    percentages = missing_data(df)
    print(f'Percentages of NA per column={percentages}')

##################Function to get timings
import time

def execute_python_script(python_file):
    t0 = time.time()
    #command = f'python {python_file}'
    #return_value = os.system(command)
    parameters = ['python', python_file]
    output = execute_command(parameters)
    dt = time.time() - t0
    #print(f'The command "{command}" was executed in {dt:.2f} seconds and it returned the value {return_value}.')
    return output, dt

def execution_time():
    #calculate timing of training.py and ingestion.py
    v0, dt0 = execute_python_script('training.py')
    v1, dt1 = execute_python_script('ingestion.py')
    return [dt0, dt1]
    #return a list of 2 timing values in seconds
    
def test_execution_time():
    [dt0, dt1] = execution_time()
    print(f'training.py was executed in {dt0:.2f} seconds.')
    print(f'ingestion.py was executed in {dt1:.2f} seconds.')

##################Function to check dependencies
import subprocess

def execute_command(parameters):
    result = subprocess.run(parameters, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')
    
def process_pip_packages(lines):
    packages = []
    for line in lines:
        fields = line.split()
        packages.append(fields)
    return packages
    
def get_pip_packages(parameters):
    result = execute_command(parameters)
    lines = result.splitlines()
    for i in range(len(lines)):
        line = lines[i]
        if line[:4] == '----':
            return process_pip_packages(lines[i + 1:])
    return None

def parse_line(line):
    index = line.find('==')
    if index == -1: return None
    return [line[:index], line[index + 2:-1]]
    
def parse_requirements_txt():
    f = open('requirements.txt', 'r')
    lines = f.readlines()
    reqs = []
    for line in lines:
        req = parse_line(line)
        if req is None: continue
        reqs.append(req)
    return reqs

def outdated_packages_list(only_outdated = True):
    packages = {}
    reqs = parse_requirements_txt()
    for req in reqs:
       packages[req[0]] = [req[1], '', '']
    packs = get_pip_packages(['pip', 'list'])
    for pack in packs:
       name = pack[0]
       version = pack[1]
       if name in packages:
           package = packages[name]
           packages[name] = [package[0], version, version]
    packs = get_pip_packages(['pip', 'list', '--outdated'])
    for pack in packs:
       name = pack[0]
       version = pack[1]
       latest = pack[2]
       if name in packages:
           package = packages[name]
           packages[name] = [package[0], package[1], latest]
    if only_outdated:
        packages2 = {}
        for name in packages:
            package = packages[name]
            if package[1] != package[2]:
                packages2[name] = package
        return packages2
    return packages
    
def print_package(name, package):
    print(f'Package: {name}, required: {package[0]}, installed: {package[1]}, latest: {package[2]}')
    
def test_outdated_packages_list():
    packages = outdated_packages_list(only_outdated = False)
    print('ALL PACKAGES IN requirements.txt:')
    for name in packages:
        package = packages[name]
        print_package(name, package)
    print('OUTDATED PACKAGES:')
    packages = outdated_packages_list()
    for name in packages:
        package = packages[name]
        print_package(name, package)

def main():
    test_predictions()
    test_dataframe_summary()
    test_missing_data()
    test_execution_time()
    test_outdated_packages_list()

if __name__ == '__main__':
    main()    
