from flask import Flask
from flask_restful import Resource, Api
import Data
import json
# POST Request
import requests


app = Flask(__name__)
api = Api(app)

api.add_resource(Data.Data, '/data')

@app.route('/')
def hello_world():
	return 'Hello World!'
            
@app.route('/cleaned')
def cleaner(): #Get just the values for the data from the nostr relay
    data = requests.get(url="http://3.144.27.94:5000/data").text #calls our data endpoint from this api running in our aws ec2 instance
    data = data.replace("\n", "")
    data = json.loads(data)
    cleaned = []
    for event in data:
        item, location, price = event[0].split("#")[2:]

        item = item.replace("\\n", "").replace("'", "").replace('"', "")
        location = location.replace("\\n", "").replace("'", "").replace('"', "")
        price = price.replace("\\n", "").replace(price[price.index(".")+3:], "" ).replace("'", "").replace('"', "")
        cleaned.append(item, location, price)
    return cleaned

@app.route('/send')
def send(): #sends the data from the nostr relay's default sqlite database to our ComposeDB with only the information and formatting we want
    data = requests.get(url="http://3.144.27.94:5000/data").text #get data from our nostr relay's sqlite database
    data = json.loads(data)
    for event in data:
        item, location, price = event[0].split("#")[2:] #extracts and cleans nostr data

        item = item.replace("\\n", "").replace("'", "").replace('"', "")
        location = location.replace("\\n", "").replace("'", "").replace('"', "")
        price = float(price.replace("\\n", "").replace(price[price.index(".")+3:], "" ).replace("'", "").replace('"', "")) # data is clean
        
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
        
        url = "http://3.144.27.94:36593/graphql" #url for graphql editor running in our aws ec2 instance
        response = requests.post(url=url, json={"query": body, "variables":  #posts to our composedb
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
    app.run(host='127.0.0.1', port=5000)
