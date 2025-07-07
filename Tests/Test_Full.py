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
            cards_per_round = [8,7,6,6,7,8]

            for round, value in enumerate(cards_per_round):  
                my_game.playerStateManager.update_dealer_order(my_game.player_queue)
                my_game.deal_cards(amount_to_deal =value) #deals hand for next round
                my_game.start_bidding(max_cards=value, round_no=round+1) 
                for _ in range(value):
                    my_game.start_round(max_cards=round)
                
