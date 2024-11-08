from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your OANDA API and account details
OANDA_API_URL = "https://api-fxpractice.oanda.com/v3/accounts/101-004-27375308-001/orders"
OANDA_API_KEY = os.getenv("d5f0fb10b45beb10148a0c052ddbb8f6-40a811e25ad56a1464a8e5b3e8bf5e21")

# Function to send a trade order to OANDA
def place_order(instrument, units, side):
    headers = {
        "Authorization": f"Bearer {OANDA_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "order": {
            "instrument": instrument,
            "units": str(units),
            "side": side,
            "type": "market",
            "timeInForce": "FOK"
        }
    }
    response = requests.post(OANDA_API_URL, headers=headers, json=data)
    return response.json()

# Webhook route to receive TradingView alerts
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get("action")
    symbol = data.get("symbol", "EUR_USD")  # Default to EUR/USD, or set dynamically

    if action == "buy":
        order_response = place_order(symbol, 100, "buy")
        return jsonify({"message": "Buy order placed", "response": order_response})
    elif action == "sell":
        order_response = place_order(symbol, -100, "sell")
        return jsonify({"message": "Sell order placed", "response": order_response})
    else:
        return jsonify({"error": "Invalid action"}), 400
