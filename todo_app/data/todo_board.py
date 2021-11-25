import os, requests, pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')

client = pymongo.MongoClient(os.getenv('DB_CONNECTION_URL'))
db = client[os.getenv('TODO_DB_NAME')]

class ToDoBoard:

    cards = []

    def __init__(self, board_id):
        self.board_id = board_id

    def parse_get_cards_response(self,get_cards_response):
        self.cards = []
        for card in get_cards_response:
            self.cards += [Card(card['_id'],card['boardId'],card['status'],card['name'])]
        return self.cards

    def get_cards(self):
        cards_json = db.cards.find({"boardId": self.board_id})
        return self.parse_get_cards_response(cards_json)

    def create_card(self,title,status):
        card = {"boardId": self.board_id,"status": status,"name":title}
        card_id = db.cards.insert_one(card).inserted_id
        return card_id

    def update_card_status(self,card_id,status):
        return db.cards.update({'_id': ObjectId(card_id)},  {'$set': {"status": status}}) 

    def parse_create_board_response(create_board_response):
        return ToDoBoard(create_board_response['id'])

    def create_board(board_name):
        board_url = 'https://api.trello.com/1/boards/'
        create_board_response = requests.post(board_url, params={ 'key':trello_key,  'token' : trello_token, 'name' : board_name, 'defaultLists' : 'false'})
        return ToDoBoard.parse_create_board_response(create_board_response.json())

    def delete_board(self):
        board_url = 'https://api.trello.com/1/boards/' + self.board_id
        delete_board_response = requests.delete(board_url, params={ 'key':trello_key,  'token' : trello_token})
        return delete_board_response.status_code==200

class Card:
    def __init__(self, card_id, board_id, status, name):
        self.card_id = card_id
        self.board_id = board_id
        self.status = status
        self.name = name

