import requests

INT_URL = 'https://int.bearer.sh/api/v4/functions/backend/'

class Client():
    """Bearer http client"""

    def __init__(self, token: str):
        self.token = token

    def call(self, integrationUuid: str, functionName: str, options: object = {}):
        headers = {'Authorization': self.token}
        response = requests.post(
            INT_URL + integrationUuid + '/' + functionName, headers=headers, data=options)
        return response.json()
