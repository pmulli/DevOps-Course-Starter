import os, pymongo
from bson.objectid import ObjectId

def getDB():
    client = pymongo.MongoClient(os.getenv('DB_CONNECTION_URL'))
    db = client[os.getenv('TODO_DB_NAME')]
    return db

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
        cards_json = getDB().cards.find({"boardId": self.board_id})
        return self.parse_get_cards_response(cards_json)

    def create_card(self,title,status):
        card = {"boardId": self.board_id,"status": status,"name":title}
        card_id = getDB().cards.insert_one(card).inserted_id
        return card_id

    def update_card_status(self,card_id,status):
        return getDB().cards.update_one({'_id': ObjectId(card_id)},  {'$set': {"status": status}}) 

class Card:
    def __init__(self, card_id, board_id, status, name):
        self.card_id = card_id
        self.board_id = board_id
        self.status = status
        self.name = name

