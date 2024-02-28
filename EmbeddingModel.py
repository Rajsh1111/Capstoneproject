import requests
import json

class EmbeddingModel:

    def __init__(self):
        # Initialize recommendation model and related resources
        pass  
    # Define the endpoint URL
    def getEmbeddings(self,input_data):
        #print(input_data)
        endpoint_url = 'http://0710b031-09b8-4daf-9a4a-4acb148de178.centralindia.azurecontainer.io/score'  # Replace <your_endpoint_url> with your actual endpoint URL
       
        # Define the input data
        if not input_data:
            input_data = {
                "data": ["pen", "pensil"]
            }
        else:
            input_data={"data":input_data}
        # Convert input data to JSON format
        input_data_json = json.dumps(input_data)
        #print(input_data_json)
        # Send POST request to the model's endpoint
        response = requests.post(endpoint_url, input_data_json)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            result = response.json()
            return result
        
            #print(result)
        else:
            print("Request failed with status code:", response.status_code)