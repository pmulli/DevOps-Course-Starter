from todo_app import app

import pytest
import dotenv
import mongomock

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)

    # Use the app to create a test_client that can be used in our tests.
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client 


def test_index_page(client):
    client.post('/items', data=dict(title='Test Card', status='To Do'))
    response = client.get('/')
    assert b"Test Card" in response.data
    

