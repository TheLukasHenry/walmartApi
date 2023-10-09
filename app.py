import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

storage_file = "alerts.json"

def load_alerts():
    if not os.path.exists(storage_file):
        return []
    with open(storage_file, "r") as file:
        try:
            alerts = json.load(file)
        except json.JSONDecodeError:
            alerts = []
    return alerts

def save_alerts(alerts):
    with open(storage_file, "w") as file:
        json.dump(alerts, file)

@app.route('/alerts', methods=['POST'])
def write_alert():
    try:
        alert_data = request.get_json(force=True)

        if not alert_data:
            return jsonify({'error': 'Invalid request body'}), 400

        alerts = load_alerts()

        alerts.append(alert_data)

        save_alerts(alerts)

        return jsonify({'alert_id': alert_data['alert_id'], 'error': ''}), 200

    except Exception as e:
        return jsonify({'alert_id': '', 'error': str(e)}), 400

@app.route('/alerts', methods=['GET'])
def read_alerts():
    try:
        service_id = request.args.get('service_id')
        start_ts = request.args.get('start_ts')
        end_ts = request.args.get('end_ts')

        if not service_id or not start_ts or not end_ts:
            return jsonify({'error': 'Missing query parameters'}), 400

        alerts = load_alerts()

        filtered_alerts = [
            alert for alert in alerts
            if alert['service_id'] == service_id and int(start_ts) <= int(alert['alert_ts']) <= int(end_ts)
        ]

        response = {
            'service_id': service_id,
            'service_name': 'my_test_service',
            'alerts': filtered_alerts,
            'error': ''
        }

        if not filtered_alerts:
            return jsonify({'error': 'No alerts found'}), 404

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)