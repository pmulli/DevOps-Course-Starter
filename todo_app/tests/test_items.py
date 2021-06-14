from todo_app.data.trello_board import TrelloBoard

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