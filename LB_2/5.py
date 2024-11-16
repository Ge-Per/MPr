from flask import Flask, request, jsonify, Response
import requests
from datetime import datetime, timedelta

app = Flask(__name__)


def get_exchange_rate(date):
    url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={date}&end={date}&valcode=usd&json'
    response = requests.get(url)

    if response.status_code == 200:
        response_json = response.json()
        if response_json:
            return response_json[0]["rate"]
    return None


@app.route("/currency", methods=["GET"])
def get_currency():
    param = request.args.get("param")

    if param not in ["today", "yesterday"]:
        return "Invalid parameter. Use 'today' or 'yesterday'.", 400

    today = datetime.today()

    if param == "today":
        date_str = today.strftime("%Y%m%d")
    elif param == "yesterday":
        yesterday = today - timedelta(days=1)
        date_str = yesterday.strftime("%Y%m%d")

    rate = get_exchange_rate(date_str)

    if rate is not None:
        data = {"currency": "USD", "rate": rate}
        content_type = request.headers.get("Content-Type")

        if content_type == "application/json":
            return jsonify(data)
        elif content_type == "application/xml":
            xml_response = (
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<response>\n"
                f"    <currency>{data['currency']}</currency>\n"
                f"    <rate>{data['rate']}</rate>\n"
                "</response>"
            )
            return Response(xml_response, mimetype="application/xml")
        else:
            return f"Currency: {data['currency']}, Rate: {data['rate']}"

    return "Error fetching exchange rate", 500


if __name__ == "__main__":
    app.run(port=8000)
