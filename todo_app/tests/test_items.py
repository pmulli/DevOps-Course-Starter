from todo_app.data.todo_board import ToDoBoard
from todo_app.data.todo_board import Card
from todo_app.app import ViewModel

class TestItems:

    board_id = "test-board-id-12345"

    @staticmethod
    def test_parse_get_cards_response():
        #Arrange
        todo_board = ToDoBoard(TestItems.board_id)
        cards_json = [{'_id': '60c71900c47a8259cb2c912d', 'boardId': TestItems.board_id, 'status': 'To Do', 'name': 'Test Card'}]

        #Act
        items = todo_board.parse_get_cards_response(cards_json)

        #Assert
        assert items[0].card_id == '60c71900c47a8259cb2c912d'

    @staticmethod
    def test_view_model_contains_items():
        #Arrange
        todo_board = ToDoBoard(TestItems.board_id)
        items = [Card('60c71900c47a8259cb2c912d',TestItems.board_id,'To Do','Test Card')]
        
        #Act
        item_view_model = ViewModel(items,'reader')

        #Assert
        assert item_view_model.items[0].card_id == '60c71900c47a8259cb2c912d'
        assert item_view_model.items[0].status == 'To Do'

    @staticmethod
    def test_view_model_categorisation():
        #Arrange
        todo_board = ToDoBoard(TestItems.board_id)
        items = [Card('60c71900c47a8259cb2c912a',TestItems.board_id,'To Do','Test To Do Card')]
        items+= [Card('60c71900c47a8259cb2c912b',TestItems.board_id,'Doing','Test Doing Card')]
        items+= [Card('60c71900c47a8259cb2c912c',TestItems.board_id,'Done','Test Done Card')]
        
        #Act
        item_view_model = ViewModel(items,'reader')

        #Assert
        assert item_view_model.todo_items[0].card_id == '60c71900c47a8259cb2c912a'
        assert item_view_model.doing_items[0].card_id == '60c71900c47a8259cb2c912b'
        assert item_view_model.done_items[0].card_id == '60c71900c47a8259cb2c912c'

