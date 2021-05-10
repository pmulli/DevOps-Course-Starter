from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data import session_items

from todo_app.data.trello_board import TrelloBoard

app = Flask(__name__)
app.config.from_object(Config)

trello_board_id = "609542268e084d62bd913af7"

@app.route('/')
def index():
    trello_board = TrelloBoard(trello_board_id)
    item_list = trello_board.get_cards()
    print(item_list)
    list_list = trello_board.get_lists()
    print(list_list)
    return render_template('index.html', itemList = item_list, listList = list_list)

 
@app.route('/items', methods=['POST'])
def add_item():
    title = request.form.get('title')
    idList = request.form.get('idList')
    trello_board = TrelloBoard(trello_board_id)
    trello_board.add_card(title, idList)

    return render_template('confirmation.html')



if __name__ == '__main__':
    app.run()
