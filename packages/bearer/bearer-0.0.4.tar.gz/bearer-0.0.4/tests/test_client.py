import pytest
import requests

from bearer.Client import Client

def test_client_init():
    client = Client('token')
    assert client.token == 'token'


def test_success_call(requests_mock):
    requests_mock.post(
        'https://int.bearer.sh/api/v4/functions/backend/integrationUuid/functionName', json={"data": "It Works!!"})
    client = Client('token')
    data = client.call('integrationId', 'functionName')
    assert data == {'data': "It Works!!"}
