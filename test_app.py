import pytest
from flask import Flask
from app import app db_conn, get_data, get_map_data

# Test configuration for Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test the database connection
def test_db_conn():
    conn = db_conn()
    assert conn is not None, "Failed to connect to the database"

# Test fetching data from tbltoilet
def test_get_data():
    data = get_data()
    assert isinstance(data, list), "Data should be a list"
    if data:
        assert isinstance(data[0], tuple), "Data rows should be tuples"

# Test fetching map data
def test_get_map_data():
    df_map = get_map_data()
    assert not df_map.empty, "DataFrame should not be empty"
    assert 'location' in df_map.columns, "DataFrame should contain 'location' column"
    assert 'longitude' in df_map.columns, "DataFrame should contain 'longitude' column"
    assert 'latitude' in df_map.columns, "DataFrame should contain 'latitude' column"

# Test the home route
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200, "Home route should return status code 200"
    assert b"Toilet Data" in response.data, "Home page should contain 'Toilet Data'"

# Test the map route
def test_map_route(client):
    response = client.get('/map')
    assert response.status_code == 200, "Map route should return status code 200"
    assert b"Map" in response.data, "Map page should contain 'Map'"
