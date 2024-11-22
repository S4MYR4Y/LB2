from flask import Flask, request
import requests


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello!!!"

    #1. Query param in URL
    #https://<IP>/data? ,? - parameter of request
    #key = value
    #key
    #2. Headers HTTP
    #  request.headers.get
@app.route("/currency", methods=['GET'])
def get_currency():

 #   print( request.headers)

  #  if "Content-Type" in request.headers.keys():
  #      if request.headers["Content-Type"] == "application/json":
  #         return "json"
  #      if request.headers["Content-Type"] == "application/xml":
  #          return "xml"

    param = request.args.get('param')

    if param == 'today' in request.args.keys():
        #  if "today" in request.args.keys():
            # if "currency" in request.args.keys():
          #  if request.args['currency'] == "usd":
                response = requests.get('https://bank.gov.ua/NBU_Exchange/exchange_site?start=20241114&end=20241114&valcode=usd&sort=exchangedate&order=desc&json')
                data = response.json()
                return data
           # elif request.args['currency'] =="eur":
              #  return "Today currency is 45"
        #return "Today"


    if param == 'yesterday' in request.args.keys():
  #  if "yesterday" in request.args.keys():
   #     if "currency" in request.args.keys():
          #  if request.args['currency'] == "usd":
                response = requests.get('https://bank.gov.ua/NBU_Exchange/exchange_site?start=20241113&end=20241113&valcode=usd&sort=exchangedate&order=desc&json')
                data = response.json()
                return data
          #  elif request.args['currency'] =="eur":
          #     return "Today currency is 45"
     #   return "Yesterday"
   # return "Default currency is 41.5"


if __name__ == '__main__':
    app.run(port=8000)
