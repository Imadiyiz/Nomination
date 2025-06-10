 # content of TestClass.py

from DeckClass import Deck
from CardClass import Card
from PlayerClass import Player
from ScoreboardClass import Scoreboard
from TableClass import Table
import pytest


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
        my_scoreboard=Scoreboard(my_player,player2)
        assert type(my_scoreboard.display()) == dict
        
class TestTableClass():

    def test_table_generation(self, my_table):
        assert my_table.stack.qsize() == 0
        assert my_table.winning_suit == None