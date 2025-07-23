#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests
import json
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Zammad credentials
ZAMMAD_URL = "https://example-domain.zammad.com/api/v1/tickets"
ZAMMAD_TOKEN = "<tokken>"  # Replace with your Zammad API token
ZAMMAD_CUSTOMER_EMAIL = "example@telusinternational.com"  # Replace with the email of the customer
ZAMMAD_GROUP_ID = 1  # "Users" group
ZAMMAD_PRIORITY_ID = 2  # Normal priority
ZAMMAD_STATE = "new"

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.json

    if not data or "alerts" not in data:
        logging.warning("❌ Invalid alert payload received: %s", data)
        return jsonify({"error": "Invalid payload"}), 400

    for alert in data["alerts"]:
        title = alert.get("labels", {}).get("alertname", "Prometheus Alert")
        description = alert.get("annotations", {}).get("description", "No description provided.")
        summary = alert.get("annotations", {}).get("summary", "No summary provided.")
        severity = alert.get("labels", {}).get("severity", "info")

        alert_body = f"""🚨 **Prometheus Alert**
Alert Name: {title}
Severity: {severity}
Summary: {summary}
Description: {description}

Full Alert Payload:
{json.dumps(alert, indent=2)}
"""

        payload = {
            "title": title,
            "group_id": ZAMMAD_GROUP_ID,
            "article": {
                "subject": f"[{severity.upper()}] {title}",
                "body": alert_body,
                "type": "note"
            },
            "customer": ZAMMAD_CUSTOMER_EMAIL,
            "priority_id": ZAMMAD_PRIORITY_ID,
            "state": ZAMMAD_STATE
        }

        headers = {
            "Authorization": f"Token token={ZAMMAD_TOKEN}",
            "Content-Type": "application/json"
        }

        logging.info("🔔 Received Alert:\n%s", json.dumps(alert, indent=2))
        logging.info("📤 Sending to Zammad:\n%s", json.dumps(payload, indent=2))

        try:
            response = requests.post(ZAMMAD_URL, json=payload, headers=headers)
            response.raise_for_status()
            logging.info("✅ Zammad API Response [%s]: %s", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            logging.error("❌ Zammad API call failed: %s", e)
            logging.error("📬 Response: %s", response.text if 'response' in locals() else "No response")
            return jsonify({"error": "Failed to create Zammad ticket"}), 500

    return jsonify({"status": "processed"}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Run Flask app on all interfaces, port 5001
    app.run(host="0.0.0.0", port=5001)
