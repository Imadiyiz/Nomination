 # content of TestClass.py

from Classes.DeckClass import Deck
from Classes.CardClass import Card
from Classes.PlayerClass import Player
from Classes.ScoreboardClass import Scoreboard
from Classes.TableClass import Table
import pytest
from Classes.GameManager import Game


#NEED TO TEST EVERY SINGLE FUNCTION FOR THE DECK
#CURRENT CAN REMOVE AND FIND CARDS IN THE DECK

# ALL TESTS MUST START WITH THE 'TEST' PREFIX

# Do not need to keep repeating the initialisation of the Deck object   
@pytest.fixture 
def my_deck():
    deck = Deck()
    return deck

@pytest.fixture 
def my_table():
    table = Table(max_players=4)
    return table

@pytest.fixture 
def my_player():
    player = Player()
    return player

@pytest.fixture 
def my_card():
    card = Card(suit=("Diamond", "♦"), value=("10", 10))
    return card

@pytest.fixture 
def my_game():
    player = Player(name="Jay", computer=False)
    player2 = Player(name="Haider", computer=False)
    player3 = Player()
    player4 = Player()
    my_list = [player, player2, player3, player4]
    game = Game(my_list)
    game.create_game()
    return game



class TestClass:

    """Class for checking the assigning of the cards"""

    def test_card_owner(self, my_card, my_player):
        test_card = Card(("Diamond", ""), ("10", 10), my_player)
        assert test_card.owner == my_player


    def test_card(self, my_card):
        assert my_card.suit == ("Diamond", "♦")
        assert my_card.value == ("10", 10)
        assert my_card.value[1] == 10
    

class TestDeckClass:

    """
    Class for testing the functionality of the DeckManager class
    """

    def test_deck_generation(self, my_deck):
        assert len(my_deck.deck) == 52
        assert type(my_deck.deck) == list

    def test_deck_card_find(self,my_deck): # will fix this later
        assert my_deck.find_card("Spade", "5") == True
        assert my_deck.find_card("Heart", "5") == True
        assert my_deck.find_card("Club", "5") == True
        assert my_deck.find_card("Diamond", "5") == True
        assert my_deck.find_card("Spacee", "ace") == False
        assert my_deck.find_card("club", "Jack") == True
        assert my_deck.find_card("spade", "Qeeun") == False
        assert my_deck.find_card("Heart", "14") == False
        assert my_deck.find_card("diamonD", "15") == False
        assert my_deck.find_card("clubs", "Twelve") == False

    def test_card_removal(self, my_deck): 
        my_deck.remove_card("Diamond", "10")
        assert my_deck.find_card("Diamond", "10") == False
    

class TestScoreboardClass():
    """
    Class for testing the functionality of the Scoreboard class
    """

    def test_scoreboard_generation(self, my_player):
        player2 = Player()
        player_list = [my_player, player2]
        my_scoreboard=Scoreboard(player_list)
        assert type(my_scoreboard.display()) == dict
        assert len(my_scoreboard.display()) == 2

class TestPlayerClass():
    """
    Class for testing the functionality of the Player class
    """

    def test_player_hand_collection(self, my_player, my_deck):
        my_player.collect_hand(my_deck.generate_hand(6))
        assert len(my_player.hand) == 6
        assert type(my_player.hand) == list

    def test_player_hidden_hand(self, my_player, my_deck):
        my_player.collect_hand(my_deck.generate_hand(6))
        assert my_player.hidden_hand == ['X','X','X','X','X','X']

        
class TestTableClass():

    def test_table_generation(self, my_table):
        assert my_table.stack.qsize() == 0
        assert my_table.winning_suit == None

class TestGameClass():
    """
    Class for testing the functionality of the Game class
    """

    def test_game_generation(self, my_game):
        assert my_game.game_state == "CREATE_GAME"
        assert my_game.player_queue.qsize() == 4
        my_game.deck.remove_card("Diamond", "10")
        assert my_game.deck.find_card("Diamond", "10") == False

    def test_game_bidding(self, my_game):
        assert my_game.player_list != []
        for player in my_game.player_list:
            assert player.bid == 0
        my_game.start_bidding(max_cards=8)
        assert my_game.player_list != []
        assert my_game.player_list[-1].handicapped_bid == True
        assert my_game.player_list[0].handicapped_bid == False

