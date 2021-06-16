from todo_app.data.trello_board import TrelloBoard
from todo_app.data.trello_board import Card
from todo_app.data.trello_board import List
from todo_app.app import ViewModel
from todo_app import app
from unittest.mock import patch
from unittest.mock import Mock

import pytest
import dotenv
import json

class TestIntegration:

    trello_board_id = "609542268e084d62bd913af7"

    sample_trello_lists_response = [{'id': '609542268e084d62bd913af8', 'name': 'To Do'}]

    @pytest.fixture
    def client(url):
        # Use our test integration config instead of the 'real' version
        file_path = dotenv.find_dotenv('.env.test')
        dotenv.load_dotenv(file_path, override=True)
 
        # Create the new app.
        test_app = app.create_app()
 
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

    @patch('requests.get', side_effect=self.mock_get_lists)
    def test_index_page(mock_get_requests, client):
        # Replace call to requests.get(url) with our own function
        mock_get_requests.side_effect = TestIntegration.mock_get_lists(f'https://api.trello.com/1/boards/{TestIntegration.trello_board_id}/lists', None)
        response = client.get('/')
        #assert response[0]['id'] == '609542268e084d62bd913af8'
        assert mock_get_requests.side_effect.json.return_value[0]['id'] == '609542268e084d62bd913af8'
        
    def mock_get_lists(url, params):
        if url == f'https://api.trello.com/1/boards/{TestIntegration.trello_board_id}/lists':
            response = Mock()
            
            # sample_trello_lists_response should point to some test response data
            response.json.return_value = TestIntegration.sample_trello_lists_response
            return response
        return None

 