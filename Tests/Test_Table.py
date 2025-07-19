from Classes.DeckClass import Deck
from Classes.CardClass import Card
from Classes.PlayerClass import Player
from Classes.ScoreboardClass import Scoreboard
from Classes.TableClass import Table
import pytest
from Classes.GameManager import Game
from Classes.UIManager import UIManager
from Classes.BiddingManager import BiddingManager
import random

@pytest.fixtures
def computer_players():
    players = []
    for i in range(5):
        players.append(Player(name=f"Player{i}"))
    return players

@pytest.fixture
def tb():
    return Table()

@pytest.fixture
def c():
    return Card(suit=("Diamond", "♦"), value=("10", 10))


class Test_Table():
    
    def test_display_stack(self, tb):
        tb.stack = None
        assert tb.display_stack == "Stack is currently empty"

    def test_add_to_stack(self, tb, c):
        
        tb.add_to_stack(card = c)
        assert c in tb.stack

    @pytest.mark.parametize
    "cards","trump_suit", "expected_bool"

    def test_verify_winner(self, tb, computer_players):
        pass

    def test_valid_add_to_stack(self, tb, computer_players):
        pass

    def test_reset_table(self, tb,c):
        
        tb.stack = [c]
        tb.reset_table()
        assert not tb.stack