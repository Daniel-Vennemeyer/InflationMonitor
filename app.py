from flask import Flask
from flask_restful import Resource, Api
import Data
import json
# POST Request
import requests
 
url = "http://3.133.141.64:46637/graphql"


app = Flask(__name__)
api = Api(app)

api.add_resource(Data.Data, '/data')

@app.route('/')
def hello_world():
	return 'Hello World!'
            
@app.route('/cleaned')
def cleaner():
    #   data, response_code = Data.Data.get()
    data = [["{\"id\":\"2da28fdfb8d55a2c97d8e8ee41773eb5fc87297b90d42a3e95cac06875c52f48\",\"pubkey\":\"f38aef9a9a6fadc53fd17fe8e8caed9ed77571c527df223d69cdb48f85e9989a\",\"created_at\":1677969607,\"kind\":1,\"tags\":[],\"content\":\"#inflationMonitor\\n#Diet Coke\\n#Denver, CO\\n#3.49\",\"sig\":\"4d7c5aa610abf00e18941b360ab2d0dfaaa8db18020a44023972aea877effe084c91c7021078daaa7cb204c5bb2d8ac4b0a1fe34ce9e525eed2bc3e5244dcb6d\"}"]]
    for event in data[0]:
        event = json.loads(event)
        item, location, price = event['content'].split("#")[1:]

        item.replace("\n", "")
        location.replace("\n", "")
        price.replace("\n", "")
    ...

@app.route('/send')
def send():
    data = [["{\"id\":\"2da28fdfb8d55a2c97d8e8ee41773eb5fc87297b90d42a3e95cac06875c52f48\",\"pubkey\":\"f38aef9a9a6fadc53fd17fe8e8caed9ed77571c527df223d69cdb48f85e9989a\",\"created_at\":1677969607,\"kind\":1,\"tags\":[],\"content\":\"#inflationMonitor\\n#Diet Coke\\n#Denver, CO\\n#3.49\",\"sig\":\"4d7c5aa610abf00e18941b360ab2d0dfaaa8db18020a44023972aea877effe084c91c7021078daaa7cb204c5bb2d8ac4b0a1fe34ce9e525eed2bc3e5244dcb6d\"}"]]
    for event in data[0]:
        event = json.loads(event)
        item, location, price = event['content'].split("#")[1:]

        item.replace("\n", "")
        location.replace("\n", "")
        price.replace("\n", "")
        body = """
        mutation CreatePriceData($i:CreatePriceDataInput!){
            createPriceData(input: $i){
                document{
                    item
                    location
                    price
        }
    }
    }
        """
        
        response = requests.post(url=url, json={"query": body, "variables": 
            {
            "i":
                    {"content": {
                        "item": item,
                        "location": location,
                        "price": price
                    }
            }
        }})
        print("response status code: ", response.status_code)
        if response.status_code == 200:
            print("response : ",response.content)
        print(response.text)


if __name__ == '__main__':
    # send()
    #  cleaner()
    app.run(host='127.0.0.1', port=5000)
