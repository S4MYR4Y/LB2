from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello!"

@app.route("/currency", methods=['GET'])
def get_currency():
    param = request.args.get('param')

    # Validate and handle supported parameters (today, yesterday)
    if param not in ['today', 'yesterday']:
        return jsonify({"error": "Invalid parameter. Valid values: 'today' , 'yesterday'."}), 400

    # Base URL for NBU API requests with appropriate parameters
    base_url = "https://bank.gov.ua/NBU_Exchange/exchange_site?"

    # Define date parameters based on the request
    today = datetime.date.today().strftime('%Y%m%d')
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')

    if param == 'today':
        url = f"{base_url}start={today}&end={today}&valcode=usd&sort=exchangedate&order=desc&json"
    else:
        url = f"{base_url}start={yesterday}&end={yesterday}&valcode=usd&sort=exchangedate&order=desc&json"

    # Fetch data from NBU API
    response = requests.get(url)
    if not response.ok:
        return jsonify({"error": f"Failed to fetch data from NBU API (status code: {response.status_code})"}), 500

    # Extract currency data (assuming USD in this case)
    data = response.json()
    try:
        usd_rate = data[0]['rate']  # Access the USD rate from the first element
        return jsonify({"currency": "USD", "rate": usd_rate, "date": data[0]['exchangedate']})
    except (IndexError, KeyError) as e:
        return jsonify({"error": f"Error parsing NBU API response: {e}"}), 500

if __name__ == '__main__':
    from datetime import datetime  # Import datetime for date calculations
    app.run(port=8000)