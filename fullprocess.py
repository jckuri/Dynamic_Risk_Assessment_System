import training
import scoring
import deployment
import diagnostics
import reporting
import json
import os

def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

##################Check and read new data

#first, read ingestedfiles.txt
import ingestion

def read_ingested_files():
    filename = os.path.join(load_config()['prod_deployment_path'], 'ingestedfiles.txt')
    try: 
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        lines = [line[:-1] for line in lines]
        return lines
    except:
        return []
    
#second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt
def get_current_csv_files():
    return ingestion.get_csv_files(load_config()['input_folder_path'])
    
def get_new_csv_files():
    csv_files = get_current_csv_files()
    ingested_files = read_ingested_files()
    for ingested_file in ingested_files:
        if ingested_file in csv_files:
            csv_files.remove(ingested_file)
    return csv_files                

##################Deciding whether to proceed, part 1
#if you found new data, you should proceed. otherwise, do end the process here

##################Checking for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data

drift_must_improve_score = False #True #False

def check_for_model_drift():
    score0 = scoring.read_f1_score(load_config()['prod_deployment_path'], 'latestscore.txt')
    print(f'score0={score0}')    
    os.system('python training.py')
    os.system('python scoring.py')
    score1 = scoring.read_f1_score(load_config()['output_model_path'], 'latestscore.txt')
    print(f'score0={score0}, score1={score1}')    
    return (score1 > score0) if drift_must_improve_score else abs(score1 - score0) > 0.001
    
##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here

def run_python_script(script):
    print(f'===== RUNNING PYTHON SCRIPT {script} =====')
    os.system(f'python {script}')

def final_process():
    run_python_script('deployment.py')
    run_python_script('apicalls.py')
    run_python_script('reporting.py')

def full_process():
    new_csv_files = get_new_csv_files()
    print(f'new_csv_files={new_csv_files}')
    if len(new_csv_files) > 0:
        print('---------------------------------------------------------')
        print('There are new CSV files. Running the script ingestion.py.')
        print('---------------------------------------------------------')
        run_python_script('ingestion.py')
        print(f'===== TESTING FOR DRIFT =====')
        drift = check_for_model_drift()
        if drift:
            print('---------------------------------------------------------------------------------')
            print('There is drift. Running the scripts deployment.py, apicalls.py, and reporting.py.')
            print('---------------------------------------------------------------------------------')
            final_process()
        else:
            print('There is no drift. Process ended.')
    else:
        print('There are no new CSV files. Process ended.')

full_process()            

##################Re-deployment
#if you found evidence for model drift, re-run the deployment.py script

##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model
