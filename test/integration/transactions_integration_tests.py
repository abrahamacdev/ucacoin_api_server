
import unittest

import requests

import constants

TOKEN = "5fd924625f6ab16a19cc9807c7c506ae1813490e4ba675f843d5a10e0baacdb8"
PRIVATE_KEY = "e39a1ca80a756fe4f460ca69b2639eb8661cfdf443ea51f861d14fbc2d65f8fc"

SERVER_IP = constants.BLOCKCHAIN_API_IP

class TransactionsIntegrationTests(unittest.TestCase):

    def test_cannot_send_more_than_i_have(self):

        # Lo registramos en la blockchain
        body = {
            "token": TOKEN,
            "receptor": "pepito",
            "cantidad": 99999999999999999.0
        }

        # Peticion http a la blockchain
        url = constants.HTTP_PROTOCOL + SERVER_IP + str(constants.SERVER_PORT) + "/enviar"

        try:
            response = requests.post(url, json=body)

            self.assertEqual(response.status_code, 500)

        except Exception as e:
            self.assertTrue(False)


    def test_cannot_send_to_inexistent_user(self):

        # Lo registramos en la blockchain
        body = {
            "token": TOKEN,
            "receptor": "xxtentation",
            "cantidad": 10.0
        }

        # Peticion http a la blockchain
        url = constants.HTTP_PROTOCOL + SERVER_IP + str(constants.SERVER_PORT) + "/enviar"

        try:
            response = requests.post(url, json=body)

            self.assertEqual(response.status_code, 400)

        except Exception as e:
            self.assertTrue(False)


    def test_cannot_send_negative_quantity(self):

        # Lo registramos en la blockchain
        body = {
            "token": TOKEN,
            "receptor": "pepito",
            "cantidad": -10.0
        }

        # Peticion http a la blockchain
        url = constants.HTTP_PROTOCOL + SERVER_IP + str(constants.SERVER_PORT) + "/enviar"

        try:
            response = requests.post(url, json=body)

            self.assertEqual(response.status_code, 400)

        except Exception as e:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()