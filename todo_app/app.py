from flask import Flask, render_template, request, redirect

from todo_app.flask_config import Config

from todo_app.data.todo_board import ToDoBoard

import os

from flask_login import LoginManager, login_required
from oauthlib.oauth2 import WebApplicationClient
import requests
import sys

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    todo_board_id = os.getenv('TODO_BOARD_ID')
    github_client_id = os.getenv('CLIENT_ID')
    github_client_secret = os.getenv('CLIENT_SECRET')

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(github_client_id)
        return redirect(client.prepare_request_uri('https://github.com/login/oauth/authorize'))
        
    @login_manager.user_loader
    def load_user(user_id):
        return None

    login_manager.init_app(app) 

    @app.route('/login/callback')
    def login():
        request_code = request.args.get('code')
        client = WebApplicationClient(github_client_id)
        data={'client_id': github_client_id, 'client_secret': github_client_secret, 'code': request_code}
        resp = requests.post('https://github.com/login/oauth/access_token', data)
        print(resp.text, file=sys.stdout)
        #client.parse_request_body_response(resp)
        return redirect('/error')

    @app.route('/')
    @login_required
    def index():
        todo_board = ToDoBoard(todo_board_id)
        items = todo_board.get_cards()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    
    @app.route('/items', methods=['POST'])
    @login_required
    def add_item():
        title = request.form.get('title')
        status = request.form.get('status')
        todo_board = ToDoBoard(todo_board_id)
        todo_board.create_card(title, status)

        items = todo_board.get_cards()
        item_view_model = ViewModel(items)
        return redirect('/')

    @app.route('/items/<item_id>')
    @login_required
    def update_item_status(item_id):    
        status = request.args.get('status')
        todo_board = ToDoBoard(todo_board_id)
        todo_board.update_card_status(item_id, status)

        items = todo_board.get_cards()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    if __name__ == '__main__':
        app.run()

    return app

class ViewModel:
    def __init__(self, items):
        self._items = items
        self._todo_items = []
        self._doing_items = []
        self._done_items = []
        self.categorise()
        
    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return self._todo_items

    @property
    def doing_items(self):
        return self._doing_items

    @property
    def done_items(self):
        return self._done_items
   
    def categorise(self):
        for item in self._items:
            if item.status == 'To Do':
                self._todo_items+=[item]
            elif item.status == 'Doing':
                self._doing_items+=[item]
            elif item.status == 'Done':
                self._done_items+=[item]
