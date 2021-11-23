import os
from threading import Thread
from todo_app import app
from todo_app.data.todo_board import ToDoBoard
import pytest
from selenium import webdriver
from dotenv import load_dotenv

test_card_name = 'Test Card'

@pytest.fixture(scope="module")
def test_env_variable():
    try:
        load_dotenv(override=True)
    except OSError:
        print("Failed to load dotenv")

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver
        
@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver
 
@pytest.fixture(scope="module")
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    todo_board = ToDoBoard.create_board('Test Board')
    os.environ['TODO_BOARD_ID'] = todo_board.board_id

    # Add item and check it appears on the page
    test_to_do_list_id = todo_board.create_list('To Do')
    os.environ['test_to_do_list_id'] = test_to_do_list_id
    test_done_list_id = todo_board.create_list('Done')
    os.environ['test_done_list_id'] = test_done_list_id
    todo_board.create_card(test_card_name, test_to_do_list_id)
    todo_board.get_cards()

    # construct the new application
    application = app.create_app()

    # start the app in its own thread.
    thread = Thread(target=lambda:
    application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    todo_board.delete_board()

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    #Check added card appears on page
    assert test_card_name in driver.page_source

    #Change list dropdown and check it has changed
    driver.find_element_by_xpath("//select[@name='idList']/option[@value='"+os.environ['test_done_list_id']+"']").click()
    assert driver.find_element_by_id('idList').get_attribute('value') == os.environ['test_done_list_id']