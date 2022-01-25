import os
from threading import Thread
from todo_app import app
from todo_app.data.todo_board import ToDoBoard
import pytest
from selenium import webdriver
from dotenv import load_dotenv
import pymongo

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
    # Can't get it working from .env.test
    os.environ['LOGIN_DISABLED'] = 'True'

    os.environ['TODO_DB_NAME'] = 'test-todo'
    todo_board = ToDoBoard('Test Board')
    os.environ['TODO_BOARD_ID'] = todo_board.board_id
    test_to_do_status = 'To Do'
    os.environ['test_to_do_status'] = test_to_do_status
    test_done_status = 'Done'
    os.environ['test_done_status'] = test_done_status

    # Add item and check it appears on the page
    todo_board.create_card(test_card_name, test_to_do_status)
    todo_board.get_cards()

    # construct the new application
    application = app.create_app()
    
    application.config['LOGIN_DISABLED'] = (os.environ['LOGIN_DISABLED'] == 'True')

    # start the app in its own thread.
    thread = Thread(target=lambda:
    application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    client = pymongo.MongoClient(os.getenv('DB_CONNECTION_URL'))
    client.drop_database(os.getenv('TODO_DB_NAME'))

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    #Check added card appears on page
    assert test_card_name in driver.page_source

    #Change list dropdown and check it has changed
    driver.find_element_by_xpath("//select[@name='status']/option[@value='"+os.environ['test_done_status']+"']").click()
    assert driver.find_element_by_id('status').get_attribute('value') == os.environ['test_done_status']