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

    def reorder_current_bids(self, player_queue: list):
        """
        Function for reordering the current bids dictionary based on the turn order
        Ideally meant to be used once before the round commenences

        Args:
            player_queue (list): The player queue is necessary to preserve the correct order
        """

        temp_dict = {}
        for player in player_queue:
            if player.bid > -1:
                temp_dict[player.name] = player.bid
            else:
                temp_dict[player.name] = 'X'
        self.current_bids = temp_dict

    def update_current_bids(self):
        """
        Function for updating the current bids scoreboard ensuring it stays in sync
        """
        for player in self.players:
            if player.bid > -1:
                self.current_bids[player.name] = player.bid
    
    def successful_player_bid(self, player: Player, not_allowed: int = -1, bid_amount: int = 0) -> bool:
        """
        Completes the player bid and updates the player objects

        Returns True or False based on whether the bid is successful
        """
        player.bid = bid_amount
        self.current_bids[player.name] = player.bid

        if player.handicapped_bid:
            if bid_amount == not_allowed:
                return False
        if 0 <= bid_amount < 9:
            player.bid = bid_amount
            self.current_bids[player.name] = bid_amount
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
        for number in self.current_bids.values():
            if number != 'X' and number >= 0:
                banned += int(number)
        banned = max_cards - banned  

        return banned
    

    #testing time !!