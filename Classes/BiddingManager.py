# Contents for the Bidding Manager python file

from .PlayerClass import Player
from Utils.tools import clear_screen
from .GameManager import UIManager


class BiddingManager():
    """
    Manages the flow of the bidding logic for players
    """

    def __init__(self,players, max_cards: int = 8):
        self.current_bids = {}
        self.players = players
        self.current = 0
        self.passed = set() #completed players
        self.not_allowed = -1
        self.max_cards = max_cards

        #bids start with 'X'
        self.current_bids = {p.name: 'X' for p in players}

    def update_current_bids(self):
        """
        Function for updating the current bids scoreboard ensuring it stays in sync
        """
        for player in self.players:
            if player.bid > -1:
                self.current_bids[player.name] = player.bid
    
    def player_bid(self, player: Player, not_allowed: int = -1, amount: int = 0) -> bool:
        """
        Completes the player bid and updates the player objects

        Returns True or False based on whether the bid is successful
        """
        player.bid = amount
        self.current_bids[player.name] = player.bid

        if player.handicapped_bid:
            if amount == not_allowed:
                return False
        if 0 <= amount < 9:
            player.bid = amount
            self.current_bids[player.name] = amount
            return True
        return False

    def reset_bids(self):
        for player in self.players:
            player.reset_bid()
            self.current_bids[player.name] = 'X'
        
    def calculate_banned_number(self, max_cards):
        """
        Function for calculating the banned number the player is unable to bid this round
        """

        banned = int()
        #calculate banned number
        print("VALUES")
        for value in self.current_bids.values():
            print(value)
        for number in self.current_bids.values():
            if number != 'X' and number >= 0:
                banned += int(number)
        banned = max_cards - banned  

        return banned