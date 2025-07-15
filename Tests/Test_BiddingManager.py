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

@pytest.fixture
def players():
    players = []
    for i in range(5):
        players.append(Player(name=f"Player{i}"))
    return players

@pytest.fixture
def bm(players):
    """
    Bidding Manager reusable object
    """
    _bm = BiddingManager(players)
    return _bm
    

class TestBiddingManager():

    def test_successful_player_bid(self, bm, players):

        #Not allowed works
        handicapped_player = players[-1]
        handicapped_player.handicapped_bid = True
        assert bm.successful_player_bid(players[0], not_allowed=2, bid_amount=2) # not handicapped
        assert not bm.successful_player_bid(handicapped_player, not_allowed=2, bid_amount=2)  # handicapped
        assert handicapped_player.bid != 2
        assert bm.successful_player_bid(players[0], not_allowed=3, bid_amount=2) 
        assert not bm.successful_player_bid(handicapped_player, not_allowed=3, bid_amount=10) 
        assert handicapped_player.bid != 10
        assert handicapped_player.bid == -1
        assert bm.successful_player_bid(handicapped_player, not_allowed=3, bid_amount=2) 
        assert handicapped_player.bid == 2

    def test_reset_bids(self, bm):
        
        for player in bm.players:
            player.bid = random.randint(1,5)

        for player in bm.players:
            assert player.bid > 0

        bm.reset_bids()

        for player in bm.players:
            assert player.bid == -1


    def test_calculate_banned_numbers(self, bm, players):
        players[0].bid = 2
        players[1].bid = 3
        bm.update_current_bids()
        banned = bm.calculate_banned_number(max_cards=8)
        assert banned == 3  # 8 - (2+3)
    