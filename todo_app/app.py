from flask import Flask, render_template, request

from todo_app.flask_config import Config

from todo_app.data import session_items


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    itemList = session_items.get_items()
    return render_template('index.html', itemList = itemList)

 
@app.route('/items', methods=['POST'])
def add_item():
    title = request.form.get('title')
    session_items.add_item(title)
    return render_template('confirmation.html')



if __name__ == '__main__':
    app.run()
