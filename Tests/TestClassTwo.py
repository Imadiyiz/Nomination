 # content of TestClassTwo.py

from Classes.DeckClass import Deck
from Classes.CardClass import Card
from Classes.PlayerClass import Player
from Classes.ScoreboardClass import Scoreboard
from Classes.TableClass import Table
import pytest
from Classes.GameManager import Game
from Classes.UIManager import UIManager
from Classes.BiddingManager import BiddingManager
from Classes.RoundManager import RoundManager


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
    player5 = Player()
    my_list = [player, player2, player3, player4, player5]
    game = Game(my_list)
    return game



class TestClass:

    def test_start_round(self,my_game):
            my_game.create_game()
            my_game.start_round(max_cards=8)
