from flask import Flask, render_template, request, redirect, flash, current_app

from todo_app.flask_config import Config

from todo_app.data.todo_board import ToDoBoard

import os

from flask_login import LoginManager, login_required, UserMixin, login_user, current_user, AnonymousUserMixin
from oauthlib.oauth2 import WebApplicationClient
from functools import wraps
import requests

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    app.logger.setLevel(os.getenv('LOG_LEVEL'))

    todo_board_id = os.getenv('TODO_BOARD_ID')
    github_client_id = os.getenv('CLIENT_ID')
    github_client_secret = os.getenv('CLIENT_SECRET')

    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    login_manager = LoginManager()
    login_manager.anonymous_user = MyCustomAnonymousUser

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(github_client_id)
        app.logger.info("User authentication error.")
        return redirect(client.prepare_request_uri('https://github.com/login/oauth/authorize'))
        
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app) 

    @app.route('/login/callback')
    def login():
        #TODO - state check
        
        request_code = request.args.get('code')
        client = WebApplicationClient(github_client_id)
        
        token_url, headers, body = client.prepare_token_request(
            'https://github.com/login/oauth/access_token',
            authorization_response=request.url,
            code=request_code,
            client_secret=github_client_secret
        )

        token_resp = requests.post(token_url, headers=headers, data=body)
        client.parse_request_body_response(token_resp.text)

        get_user_uri, headers, body = client.add_token('https://api.github.com/user')
        user_info_resp = requests.get(get_user_uri, headers=headers, data=body)
        user_id=user_info_resp.json()["id"]
        user = User(user_id)
        login_user(user)

        return redirect('/')

    @app.route('/')
    @login_required
    def index():
        todo_board = ToDoBoard(todo_board_id)
        items = todo_board.get_cards()
        app.logger.debug("TODO Items count %s", len(items))

        item_view_model = ViewModel(items, current_user.role)
        return render_template('index.html', view_model=item_view_model)

    
    @app.route('/items', methods=['POST'])
    @login_required
    @writer_required
    def add_item():
        title = request.form.get('title')
        status = request.form.get('status')
        todo_board = ToDoBoard(todo_board_id)
        try:
            item_id = todo_board.create_card(title, status)
            app.logger.info("TODO Item create success. item_id=\"%s\" name=\"%s\" status=\"%s\" user=\"%s\"", item_id, title, status, current_user.id)
        except Exception as e:
            app.logger.error("TODO Item create failed. name=\"%s\" status=\"%s\" user=\"%s\"", title, status, current_user.id)
            raise

        items = todo_board.get_cards()
        item_view_model = ViewModel(items, current_user.role)
        return redirect('/')

    @app.route('/items/<item_id>')
    @login_required
    @writer_required
    def update_item_status(item_id):    
        status = request.args.get('status')
        todo_board = ToDoBoard(todo_board_id)
        try:
            todo_board.update_card_status(item_id, status)
            app.logger.info("TODO Item update success. item_id=\"%s\" status=\"%s\" user=\"%s\"", item_id, status, current_user.id)
        except Exception as e:
            app.logger.error("TODO Item update failed. item_id=\"%s\" status=\"%s\" user=\"%s\"", item_id, status, current_user.id)
            raise

        items = todo_board.get_cards()
        item_view_model = ViewModel(items, current_user.role)
        return render_template('index.html', view_model=item_view_model)

    if __name__ == '__main__':
        app.run()

    return app

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        if id == 42806788:
            self.role = "writer"
        else:
            self.role = "reader"

    def get_id(self):
        return self.id

class MyCustomAnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.role = "writer"

def writer_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "writer":
            return f(*args, **kwargs)
        else:
            current_app.logger.warning("User not authorised to perform writer actions. user=\"%s\" role=\"%s\"", current_user.id, current_user.role)
            flash("Permission Denied: You do not have the required role to perform this action.")
            return redirect('/')

    return wrap

class ViewModel:
    def __init__(self, items, user_role):
        self._items = items
        self._todo_items = []
        self._doing_items = []
        self._done_items = []
        self.categorise()
        self._user_role = user_role
        
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

    @property
    def user_role(self):
        return self._user_role
