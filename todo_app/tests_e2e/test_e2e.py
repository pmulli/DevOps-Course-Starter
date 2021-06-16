import os
from threading import Thread
from todo_app import app
from todo_app.data.trello_board import TrelloBoard
import pytest
import dotenv
from selenium import webdriver


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver
        
@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    trello_board = TrelloBoard.create_board('Test Board')
    os.environ['TRELLO_BOARD_ID'] = trello_board.board_id

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda:
    application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    #test_task_journey(driver, app)

    # Tear Down
    thread.join(1)
    trello_board.delete_board()

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'