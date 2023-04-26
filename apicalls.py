import requests
import os
import json

def load_config():
    with open('config.json','r') as f:
        config = json.load(f) 
    return config

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000"

#Call each API endpoint and store the responses
#response1 = #put an API call here
location = str(os.path.join(load_config()['test_data_path'], 'testdata.csv'))
input1 = {'location': location}
print('INPUT 1:', input1)
response1 = requests.post(URL + '/prediction', data = json.dumps(input1))
dict1 = response1.json()
print('OUTPUT 1:', dict1)

#response2 = #put an API call here
response2 = requests.get(URL + '/scoring') #put an API call here
dict2 = response2.json()
print('OUTPUT 2:', dict2)

#response3 = #put an API call here
response3 = requests.get(URL + '/summarystats') #put an API call here
dict3 = response3.json()
print('OUTPUT 3:', dict3)

#response4 = #put an API call here
response4 = requests.get(URL + '/diagnostics') #put an API call here
dict4 = response4.json()
print('OUTPUT 4:', dict4)

#combine all API responses
#responses = #combine reponses here
responses = ''
responses += f'INPUT 1: {input1}\n'
responses += f'OUTPUT 1: {dict1}\n'
responses += f'OUTPUT 2: {dict2}\n'
responses += f'OUTPUT 3: {dict3}\n'
responses += f'OUTPUT 4: {dict4}\n'
#write the responses to your workspace
api_returns_file = os.path.join(load_config()['output_model_path'], 'apireturns.txt')
f = open(api_returns_file, 'w')
f.write(responses)
f.close()
print(f'The API returns were saved in file "{api_returns_file}".')
