import openai
import keyring
from arcgis.gis import GIS

# Credentials & Settings
service_id = 'openai-arcgis!'
password = keyring.get_password(service_id, 'howe2021') # retrieve password
openai_key = keyring.get_password(service_id, 'openai-key') 
agol_item = 'b1e6dfffe2cc4de0bf7cc0f02e861e28'
default_prompt = 'Interpret the following CSV file and tell me some insights: '
prompt_string = input('What would you like to know about your dataset? Default is to interpret an HFL: ')

# Python API
gis = GIS("https://howe2021.maps.arcgis.com/", "howe2021", password)
hfl = gis.content.get(agol_item)

# Query a FL using parameters and coverted to JSON data
# Assign a variable to the list of features in the Feature Set
feature_layer = hfl.layers[13]
feature_set = feature_layer.query(where="1=1",out_fields=['VAR_DIRECT','VAR_ROUTE','About','Shape__Len','Route_Name','Shape__Length'],return_geometry=False)
feature_list = feature_set.features
data = str(feature_list)

## OpenAI API Calls
openai.api_key = openai_key

def chatgpt_request(input_string, dataset):
  if input_string == '':
    input_string = default_prompt
    
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"{input_string} \n{dataset}",
    temperature=0.2,
    max_tokens=2049,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )

  text_output = response.choices[0].text
  return text_output

output = chatgpt_request(prompt_string, data)
print(output)