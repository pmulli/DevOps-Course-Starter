from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data import session_items

from todo_app.data.trello_board import TrelloBoard

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    trello_board = TrelloBoard("609542268e084d62bd913af7")
    item_list = trello_board.get_cards()
    print(item_list)
    list_list = trello_board.get_lists()
    print(list_list)
    return render_template('index.html', itemList = item_list, listList = list_list)

 
@app.route('/items', methods=['POST'])
def add_item():
    title = request.form.get('title')
    session_items.add_item(title)
    return render_template('confirmation.html')



if __name__ == '__main__':
    app.run()
