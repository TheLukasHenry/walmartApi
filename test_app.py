import unittest
import json
from app import app

class AlertsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_write_alert_success(self):
        data = {
            "alert_id": "b950482e9911ec7e41f7ca5e5d9a424f",
            "service_id": "my_test_service_id",
            "service_name": "my_test service",
            "model": "my_test_model",
            "alert_type": "anomaly",
            "alert_ts": "1695644160",
            "severity": "warning",
            "team_slack": "slack_ch"
        }
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/alerts', json=data, headers=headers)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['alert_id'], data['alert_id'])
        self.assertEqual(response_data['error'], '')

    def test_write_alert_invalid_request_body(self):
        headers = {'Content-Type': 'application/json'}
        response = self.app.post('/alerts', headers=headers)

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)


    def test_read_alerts_success(self):
        query_params = {
            'service_id': 'my_test_service_id',
            'start_ts': '1695643160',
            'end_ts': '1695644360'
        }

        response = self.app.get('/alerts', query_string=query_params)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['service_id'], query_params['service_id'])
        self.assertEqual(response_data['service_name'], 'my_test_service')
        self.assertIsInstance(response_data['alerts'], list)
        self.assertEqual(response_data['error'], '')

    def test_read_alerts_missing_query_parameters(self):
        response = self.app.get('/alerts')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], 'Missing query parameters')

if __name__ == '__main__':
    unittest.main()