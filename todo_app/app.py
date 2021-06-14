from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data.trello_board import TrelloBoard

app = Flask(__name__)
app.config.from_object(Config)

trello_board_id = "609542268e084d62bd913af7"

class ViewModel:
    def __init__(self, items, lists):
        self._items = items
        self._lists = lists
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

    @property
    def lists(self):
        return self._lists
    
    def categorise(self):
        for list in self._lists:
            for item in self._items:
                if item.list_id == list.list_id:
                    if list.name == 'To Do':
                        self._todo_items+=[item]
                    elif list.name == 'Doing':
                        self._doing_items+=[item]
                    elif list.name == 'Done':
                        self._done_items+=[item]

@app.route('/')
def index():
    trello_board = TrelloBoard(trello_board_id)
    items = trello_board.get_cards()
    lists = trello_board.get_lists()
    item_view_model = ViewModel(items,lists)
    return render_template('index.html', view_model=item_view_model)

 
@app.route('/items', methods=['POST'])
def add_item():
    title = request.form.get('title')
    list_id = request.form.get('idList')
    trello_board = TrelloBoard(trello_board_id)
    trello_board.add_card(title, list_id)

    items = trello_board.get_cards()
    lists = trello_board.get_lists()
    item_view_model = ViewModel(items,lists)
    return render_template('index.html', view_model=item_view_model)

@app.route('/items/<item_id>')
def update_item_status(item_id):    
    list_id = request.args.get('idList')
    trello_board = TrelloBoard(trello_board_id)
    trello_board.update_card_status(item_id, list_id)

    items = trello_board.get_cards()
    lists = trello_board.get_lists()
    item_view_model = ViewModel(items,lists)
    return render_template('index.html', view_model=item_view_model)


if __name__ == '__main__':
    app.run()
