import os, requests
from dotenv import load_dotenv

load_dotenv()

trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')

trello_board_id="609542268e084d62bd913af7"

class TrelloBoard:

    cards = []
    lists = []

    def __init__(self, board_id):
        self.board_id = board_id

    def parse_get_cards_response(self,get_cards_response):
        self.cards = []
        for card in get_cards_response:
                self.cards += [
                    {
                        "id": card['id'],
                        "idList": card['idList'],
                        "name": card['name']
                    }
                ]
        return self.cards


    def get_cards(self):
        cards_url = 'https://api.trello.com/1/boards/' + trello_board_id + '/cards'
        print(cards_url)
        get_cards_response = requests.get(cards_url, params={ 'key':trello_key,  'token' : trello_token})
        print(get_cards_response)
        print(get_cards_response.json())
        
        self.parse_get_cards_response(get_cards_response.json())

        return self.cards


    def parse_get_lists_response(self,get_lists_response):
        self.lists = []
        for list in get_lists_response:
                self.lists += [
                    {
                        "id": list['id'],
                        "name": list['name']
                    }
                ]
        return self.lists


    def get_lists(self):
        lists_url = 'https://api.trello.com/1/boards/' + trello_board_id + '/lists'
        print(lists_url)
        get_lists_response = requests.get(lists_url, params={ 'key':trello_key,  'token' : trello_token})
        
        self.parse_get_lists_response(get_lists_response.json())

        return self.lists


    def get_card(self,card_id):
        cards = self.get_cards()
        return next((card for card in cards if card['id'] == card_id), None)


    def add_card(self,title,idList):

        create_card_url = 'https://api.trello.com/1/cards'
        print(create_card_url)
        create_card_response = requests.post(create_card_url, params={ 'key':trello_key, 'token' : trello_token, 'idList' : idList, 'name' : title})
        print(create_card_response)
        return create_card_response


    def update_card(self,card_id):
        return card_id
