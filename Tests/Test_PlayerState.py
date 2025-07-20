# Contents of the PlayerState test python file

from Classes.DeckClass import Deck
from Classes.CardClass import Card
from Classes.PlayerClass import Player
from Classes.PlayerStateManager import PlayerStateManager
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
    return Table(UIManager())
    

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
    game.player_queue = [player, player2, player3, player4, player5]
    game.original_queue = [player, player2, player3, player4, player5]
    return game

class Test_PlayerState():
    """
    TEsts the functions in the PlayerStateManager class
    """

    def test_update_winning_order(self, my_game):
        """
        Determines whether the order is correctly changed should a player win the hand
        """
        player5 = my_game.player_queue[-1]
        player4 = my_game.player_queue[3]
        player3 = my_game.player_queue[2]
        player2 = my_game.player_queue[1]
        player1 = my_game.player_queue[0]
        my_game.playerStateManager.update_winner_order(winner=player5, player_queue=my_game.player_queue)
        assert my_game.player_queue[0] == player5
        assert my_game.player_queue[1] == player1
        assert my_game.player_queue[2] == player2
        assert my_game.player_queue[3] == player3
        assert my_game.player_queue[4] == player4
    
    def test_update_winning_order2(self, my_game):
        player5 = my_game.player_queue[-1]
        player4 = my_game.player_queue[3]
        player3 = my_game.player_queue[2]
        player2 = my_game.player_queue[1]
        player1 = my_game.player_queue[0]
        my_game.playerStateManager.update_winner_order(winner=player2, player_queue=my_game.player_queue)
        assert my_game.player_queue[0] == player2
        assert my_game.player_queue[1] == player3
        assert my_game.player_queue[2] == player4
        assert my_game.player_queue[3] == player5
        assert my_game.player_queue[4] == player1

    def test_update_dealer_order(self, my_game):
        """
        Determines whether the dealer shifts one position every round
        """

        player5 = my_game.player_queue[-1]
        player4 = my_game.player_queue[3]
        player3 = my_game.player_queue[2]
        player2 = my_game.player_queue[1]
        player1 = my_game.player_queue[0]

        my_game.original_queue = my_game.playerStateManager.update_dealer_order(my_game.original_queue)
        my_game.player_queue = my_game.original_queue

        assert my_game.player_queue[0] == player2
        assert my_game.player_queue[1] == player3
        assert my_game.player_queue[2] == player4
        assert my_game.player_queue[3] == player5
        assert my_game.player_queue[4] == player1
