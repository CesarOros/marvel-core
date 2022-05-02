import pytest
import requests
import json


@pytest.fixture
def main_url():
    return "http://localhost:3200"


def test_search_comics(main_url):
    response = requests.get(f"{main_url}/searchComics")
    data = json.loads(response.content)
    assert "characters" in data
    assert len(data["characters"])

    response = requests.get(
        f"{main_url}/searchComics?criteria=personajes&name_title=Iron Man"
    )
    data = json.loads(response.content)
    assert "characters" in data
    assert data["characters"][0]["name"] == "Iron Man"

    response = requests.get(
        f"{main_url}/searchComics?criteria=comics&name_title=Iron Man"
    )
    data = json.loads(response.content)
    assert "comics" in data
    assert len(data["comics"])

    response = requests.get(f"{main_url}/searchComics?name_title=Iron Man")
    data = json.loads(response.content)
    assert "comics" in data
    assert "characters" in data
