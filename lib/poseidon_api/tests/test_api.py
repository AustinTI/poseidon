import falcon
import pytest
from falcon import testing
from poseidon_api.api import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_v1(client):
    response = client.simulate_get("/v1")
    assert response.status == falcon.HTTP_OK


def test_network(client):
    response = client.simulate_get("/v1/network")
    assert len(response.json) == 2
    assert response.status == falcon.HTTP_OK


def test_network_by_ip(client):
    response = client.simulate_get("/v1/network/10.0.0.1")
    assert len(response.json["dataset"]) == 0
    assert response.status == falcon.HTTP_OK


def test_network_full(client):
    response = client.simulate_get("/v1/network_full")
    assert len(response.json) == 1
    assert response.status == falcon.HTTP_OK


def test_info(client):
    response = client.simulate_get("/v1/info")
    assert response.status == falcon.HTTP_OK
