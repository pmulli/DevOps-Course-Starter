from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data.todo_board import ToDoBoard

import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    todo_board_id = os.getenv('TODO_BOARD_ID')


    @app.route('/')
    def index():
        todo_board = ToDoBoard(todo_board_id)
        items = todo_board.get_cards()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    
    @app.route('/items', methods=['POST'])
    def add_item():
        title = request.form.get('title')
        status = request.form.get('status')
        todo_board = ToDoBoard(todo_board_id)
        todo_board.create_card(title, status)

        items = todo_board.get_cards()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/items/<item_id>')
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
