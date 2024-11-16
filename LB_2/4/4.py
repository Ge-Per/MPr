from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route("/currency", methods=["GET"])
def get_currency():
    key = request.args.get("key")
    today = request.args.get("today")

    if "today" not in request.args or not key:
        return "Invalid query parameters", 400

    data = {"currency": "USD", "rate": "41.5"}
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

if __name__ == "__main__":
    app.run(port=8000)
