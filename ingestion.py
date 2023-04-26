import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

#############Load config.json and get input and output paths
def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

from os import listdir
from os.path import isfile, join

#############Function for data ingestion
def valid_file(f):
    return f[-4:].lower() == '.csv'
    
def get_csv_files(folder):
    files = sorted(listdir(folder))
    files = [join(folder, f) for f in files]
    return [f for f in files if valid_file(f)]
    
def read_csv(f):
    return pd.read_csv(f)
    
def concatenate_and_remove_duplicates(dfs):
    if len(dfs) == 0: return None
    cdf = dfs[0]
    for i in range(1, len(dfs)):
        df = dfs[i]
        cdf = pd.concat([cdf, df])
    #print(cdf)
    return cdf.drop_duplicates(ignore_index = True)
    
def write_to_csv(df, f):
    df.to_csv(f, index = False)
    
def save_record_of_ingestion(csv_files, f):
    f = open(f, "w")
    for csv_file in csv_files:
        f.write(f'{csv_file}\n')
    f.close()
    print(f'Record of ingestion was saved in file "{f.name}".')

def merge_multiple_dataframe():
    #check for datasets, compile them together, and write to an output file
    resulting_file = join(load_config()['output_folder_path'], 'finaldata.csv')
    csv_files = get_csv_files(load_config()['input_folder_path'])
    #if os.path.exists(resulting_file): csv_files.append(resulting_file)
    print(f'csv_files={csv_files}')    
    dfs = [read_csv(f) for f in csv_files]
    for i in range(len(dfs)): 
        csv_file = csv_files[i]
        print(csv_file)
        df = dfs[i]
        print(df)
    rdf = concatenate_and_remove_duplicates(dfs)
    print(resulting_file)
    print(rdf)
    write_to_csv(rdf, resulting_file)
    record_file = join(load_config()['output_folder_path'], 'ingestedfiles.txt')
    save_record_of_ingestion(csv_files, record_file)

if __name__ == '__main__':
    merge_multiple_dataframe()
