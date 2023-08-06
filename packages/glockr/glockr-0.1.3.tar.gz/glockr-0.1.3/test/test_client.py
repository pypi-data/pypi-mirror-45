import unittest
import subprocess
import requests
import time
import json

BASE_URL = 'http://127.0.0.1:29410'


class TestClient(unittest.TestCase):
    _server_process = None

    @staticmethod
    def get_current_dict() -> dict:
        target_url = BASE_URL + '/res'
        resp = requests.get(target_url)
        resp_dict = json.loads(resp.text)
        return resp_dict

    def get_res_status(self, name) -> str:
        current_dict = self.get_current_dict()
        return current_dict[str(name)]['status']

    @classmethod
    def setUpClass(cls):
        super(TestClient, cls).setUpClass()
        cls._server_process = subprocess.Popen('glockrs', shell=True)
        time.sleep(3)

    def test_1_add(self):
        name_list = list(range(0, 30))
        for label in range(5):
            for _ in range(5):
                cmd = 'glockrc add {} {}'.format(name_list.pop(), label)
                subprocess.check_call(cmd, shell=True)

    def test_2_show_all(self):
        current_dict = self.get_current_dict()
        assert len(current_dict) == 25

    @classmethod
    def tearDownClass(cls):
        super(TestClient, cls).tearDownClass()
        cls._server_process.kill()


if __name__ == '__main__':
    unittest.main()
