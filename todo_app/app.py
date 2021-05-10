from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data import session_items

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')

@app.route('/')
def index():
    item_list = session_items.get_items()
    return render_template('index.html', itemList = item_list)

 
@app.route('/items', methods=['POST'])
def add_item():
    title = request.form.get('title')
    session_items.add_item(title)
    return render_template('confirmation.html')



if __name__ == '__main__':
    app.run()
