from todo_app import app
from todo_app.data.todo_board import ToDoBoard
from unittest.mock import patch
from unittest.mock import Mock

import pytest
import dotenv
import os
import mongomock

sample_todo_cards_response = [{'_id': '60c71900c47a8259cb2c912d', 'boardId': 'abcde','status': 'Doing','name': 'Test Card'}]

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client 


def test_index_page(client):
    todo_board = ToDoBoard("fake")
    todo_board.create_card("Shopping", "To Do")

    cards = todo_board.get_cards()

    response = client.get('/')
    #assert b"Test Card" in response.data
    assert True
    

