from todo_app.data.trello_board import TrelloBoard
from todo_app.data.trello_board import Card
from todo_app.data.trello_board import List
from todo_app.app import ViewModel

class TestItems:

    trello_board_id = "609542268e084d62bd913af7"

    @staticmethod
    def test_parse_get_cards_response():
        #Arrange
        trello_board = TrelloBoard(TestItems.trello_board_id)
        cards_json = [{'id': '60c71900c47a8259cb2c912d', 'idList': '609542268e084d62bd913af8','name': 'Test Card'}]

        #Act
        items = trello_board.parse_get_cards_response(cards_json)

        #Assert
        assert items[0].card_id == '60c71900c47a8259cb2c912d'

    @staticmethod
    def test_parse_get_lists_response():
        #Arrange
        trello_board = TrelloBoard(TestItems.trello_board_id)
        lists_json = [{'id': '609542268e084d62bd913af8', 'name': 'To Do'}]

        #Act
        lists = trello_board.parse_get_lists_response(lists_json)

        #Assert
        assert lists[0].name == 'To Do'

    @staticmethod
    def test_view_model_contains_items_and_lists():
        #Arrange
        trello_board = TrelloBoard(TestItems.trello_board_id)
        items = [Card('60c71900c47a8259cb2c912d','609542268e084d62bd913af8','Test Card')]
        lists = [List('609542268e084d62bd913af8','To Do')]
        
        #Act
        item_view_model = ViewModel(items,lists)

        #Assert
        assert item_view_model.items[0].card_id == '60c71900c47a8259cb2c912d'
        assert item_view_model.lists[0].name == 'To Do'

    @staticmethod
    def test_view_model_categorisation():
        #Arrange
        trello_board = TrelloBoard(TestItems.trello_board_id)
        items = [Card('60c71900c47a8259cb2c912a','609542268e084d62bd913af1','Test To Do Card')]
        items+= [Card('60c71900c47a8259cb2c912b','609542268e084d62bd913af2','Test Doing Card')]
        items+= [Card('60c71900c47a8259cb2c912c','609542268e084d62bd913af3','Test Done Card')]
        
        lists = [List('609542268e084d62bd913af1','To Do')]
        lists+= [List('609542268e084d62bd913af2','Doing')]
        lists+= [List('609542268e084d62bd913af3','Done')]
        
        #Act
        item_view_model = ViewModel(items,lists)

        #Assert
        assert item_view_model.todo_items[0].card_id == '60c71900c47a8259cb2c912a'
        assert item_view_model.doing_items[0].card_id == '60c71900c47a8259cb2c912b'
        assert item_view_model.done_items[0].card_id == '60c71900c47a8259cb2c912c'
