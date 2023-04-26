import json
import os

##################Load config.json and get environment variables
def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

# { "output_folder_path": "ingesteddata", "output_model_path": "models", "prod_deployment_path": "production_deployment"}
for directory in ['output_folder_path', 'output_model_path', 'prod_deployment_path']:
    os.system(f'rm {load_config()[directory]}/*.*')
os.system('./use_configuration_1.sh')
