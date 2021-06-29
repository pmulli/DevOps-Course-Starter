from todo_app import app
from unittest.mock import patch
from unittest.mock import Mock

import pytest
import dotenv
import os

sample_trello_cards_response = [{'id': '60c71900c47a8259cb2c912d', 'idList': '609542268e084d62bd913af8','name': 'Test Card'}]
sample_trello_lists_response = [{'id': '609542268e084d62bd913af8', 'name': 'Doing'}]

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get
    response = client.get('/')
    assert b"Test Card" in response.data
    
def mock_get(url, params):
    if url == f'https://api.trello.com/1/boards/'+os.environ['TRELLO_BOARD_ID']+'/cards':
        response = Mock()
        
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = sample_trello_cards_response
        return response
    elif url == f'https://api.trello.com/1/boards/'+os.environ['TRELLO_BOARD_ID']+'/lists':
        response = Mock()
        
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = sample_trello_lists_response
        return response
    return None

