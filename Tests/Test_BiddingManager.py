from Classes.DeckClass import Deck
from Classes.CardClass import Card
from Classes.PlayerClass import Player
from Classes.ScoreboardClass import Scoreboard
from Classes.TableClass import Table
import pytest
from Classes.GameManager import Game
from Classes.UIManager import UIManager
from Classes.BiddingManager import BiddingManager

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
    game.create_game()
    return game

class TestBiddingManager():

    def test_successful_player_bid(self,my_game):

        #Not allowed works
        assert my_game.biddingManager.successful_player_bid(my_game.player_queue[0], not_allowed=2, bid_amount=2) == True # not handicapped
        assert my_game.biddingManager.successful_player_bid(my_game.player_queue[-1], not_allowed=2, bid_amount=2) == False # handicapped
        assert my_game.biddingManager.successful_player_bid(my_game.player_queue[0], not_allowed=3, bid_amount=2) == True
        assert my_game.biddingManager.successful_player_bid(my_game.player_queue[0], not_allowed=3, bid_amount=10) == False

    def test_reset_bids(self, my_game):

        assert """""" ###

    