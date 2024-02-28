from flask import Flask, render_template, request
from LLMModel import LLMModel
import html
from openai import OpenAI
from flask import jsonify
import time
import uuid
import pyodbc
import os
import numpy as np
import readData as rd
from RecommendationModel import  RecommendationModel
from EmbeddingModel import EmbeddingModel
import readData as rd
import json

os.environ["OPENAI_API_KEY"] = "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"


app = Flask(__name__)

class CustomChatBot:
    def __init__(self):
        pass

    def get_response(self, statement):
        # Generate a unique ID for this API call
        api_call_id = uuid.uuid4().hex

        # Make a request to the OpenAI API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                        {
                  "role": "system",
                  "content": "Respond in a list of 10 items that matches the context of toys and stationery retail stores, without numbers. If no items found return an empty list."
                },
                {"role": "user", "content": statement}
            ],
            n=3  # Get 3 possible responses
        )

        responses = []
        if completion:
            for choice in completion.choices:
                print(choice.message.content)
                
                response = {
                'content': choice.message.content,
                'index': choice.index,
                'api_call_id': api_call_id  # Add the API call ID to the response
            }
                
                responses.append(response)  # Store HTML content in response
        else:
            print("No data found in the user input.")

        return jsonify(responses)  # Return list of responses

client = OpenAI()
# Create a new chatbot
search_bot = CustomChatBot()
#conn = sqlite3.connect('user_responses_log.db',check_same_thread=False)
# Connect to Azure SQL Database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=virtucart.database.windows.net;DATABASE=virtucart;UID=virtucart_admin;PWD=Virtu_Cart2024')

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/modelrecommendation",methods=['GET'])
def getModelRecommendations():
    stockcodes = request.args.get('stockcodes')
    recommendation_model=RecommendationModel()
    transection_df=rd.createDataFrame(rd.salesDataQuery) 
    # Get final recommendations for all the matching stockcodes
    final_recommendations = recommendation_model.get_final_recommendations(transection_df, [stockcodes])
    print(final_recommendations)
    IdNameDict={}
    for pId in final_recommendations:
        print(pId)
        pName=get_product_names(pId)
        print(pName)
        IdNameDict[pId]=pName
    print(type(IdNameDict))    
    return list(IdNameDict.items())

@app.route("/productCodes",methods=['GET'])
def getProductCodes():
    return ['15044D', '35271S', '23843']
    #return  ['https://virtucartimages.blob.core.windows.net/vimages/Pictures/15044D.png?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-06-24T21:04:59Z&st=2024-02-24T13:04:59Z&spr=https&sig=%2B%2BQnkTzwod6zc3dJtW1wCYeFXPCeK0Ij3LAYbyAxP%2BY%3D',
          #   ]


def getOpenAIRecommendations(query):
   llm_model=LLMModel()
   llm_items = llm_model.get_llm_items(query)
   if query:
       print('Request for hello page received with name=%s' % query)
       return llm_items
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return "No results found"

@app.route("/getairecommendations")
def getAIRecommendations():
   query = request.args.get('msg')
   llm_model=LLMModel()
   llm_items = llm_model.get_llm_items(query)
   if query:
       return llm_items
   else:
       return "No results found"


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    llm_items=getOpenAIRecommendations(user_text)
    embedding_model=EmbeddingModel()
    embeddings=embedding_model.getEmbeddings(llm_items)
    productIds=transposeList(embeddings['stockcodes'])
    responseJson={}
    productIdVsName={}
    flat_productIds=flatten_sum(productIds)
    responseJson['productIds']=productIds
    
    for pId in flat_productIds:
        print(pId)
        pName=get_product_names(pId)
        print(pName[0])
        productIdVsName[pId]=pName
    responseJson['IdNameMap']=productIdVsName
    print(responseJson)
    return responseJson
    #recommendations=getModelRecommendations(embeddings)
    #print((recommendations))
    #return embeddings


def flatten_sum(matrix):
     return sum(matrix, [])
    
def transposeList(stockcodes):
    for i in range(len(stockcodes)):
        while len(stockcodes[i]) < 3:
            stockcodes[i].append('no_item_found')
    transposed_array = np.array(stockcodes).T
    print(transposed_array)
    transposed_list_of_lists = transposed_array.tolist()
    print(transposed_list_of_lists)
    return transposed_list_of_lists

# Log the user like/dislike options
@app.route("/log", methods=["POST"])
def log():
    # Get the log entry from the request
    log_entry = request.form.get("logEntry").split(' | ')

    # Insert the log entry into the database
    c = conn.cursor()
    c.execute('''
        INSERT INTO logs VALUES (?,?,?,?,?)
    ''', log_entry)
    conn.commit()

    return "OK"

@app.route("/getlogs", methods=["GET"])
def get_logs():
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    logs = c.fetchall()
    return jsonify(logs)


@app.route("/getProductNames", methods=["GET"])
def get_product_names(productId):
    c = conn.cursor()
    query="select top 1 description from productmaster where stockcode='"+productId+"'"
    c.execute(query)
    result = c.fetchall()
    if result:
            productNames=(result[0][0])  # append the first element of the first tuple
    else:
            productNames="None"  # append None if there is no result
    return productNames

    



if __name__ == "__main__":
    app.run(debug=True)
