import json
from config import Config
from constants import Constants
from pathlib import Path
import requests

def load_integration_tests():
    integration_test_filepath = Path(Constants.INTEGRATION_TESTS_CASES_FILE)
    if integration_test_filepath.exists():
        with open(str(integration_test_filepath)) as f:
            return(json.load(f))
    return {}


def run_integration_tests():
    tests = load_integration_tests()
    config = Config()
    flask_config = config.get('flask', {})
    flask_host = flask_config.get('host', Constants.APP_HOST)
    flask_port = flask_config.get('port', Constants.APP_PORT)
    url = f"http://{flask_host}:{flask_port}/rates"

    for test in tests:
        test_status = 'passed'
        test_id = test['id']
        params = test['input']
        expected_output = test['expected_output']
        expected_res_code = expected_output['res_code']
        expected_res_msg = expected_output['res_msg']
        r = requests.get(url=url, params=params)
        res_code = r.status_code
        res_msg = r.json()
    
        if isinstance(res_msg, list):
            expected_res_json = json.loads(expected_res_msg)
            for i in range(len(res_msg)):
                if res_msg[i]['day'] != expected_res_json[i]['day'] or \
                    res_msg[i]['average_price'] != expected_res_json[i]['average_price']:
                    test_status = 'failed'
                    break

        else:
            if res_code != expected_res_code or res_msg != expected_res_msg:
                test_status = 'failed'
        print(f"Test ID: {test_id} {test_status}.")


if __name__ == "__main__":
    run_integration_tests()