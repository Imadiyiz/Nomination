# Contents for the Bidding Manager python file

from .PlayerClass import Player
from typing import List


class BiddingManager():
    """
    Manages the flow of the bidding logic for players
    """

    def __init__(self,players):
        self.current_bids = {}
        self.players = players
        self.current = 0
        self.not_allowed = -1
        self.current_bids = {p.name: 'X' for p in players}

    def reorder_current_bids(self, player_queue: List[Player]):
        """
        Function for reordering the current bids dictionary based on the turn order
        Ideally meant to be used once before the round commenences

        Args:
            player_queue (list[Player]): The player queue is necessary to preserve the correct order
        """

        self.current_bids = {
            player.name: player.bid if player.bid > -1 else 'X'
            for player in player_queue
        }

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

        Returns:
          bool: True if the bid is successful, False otherwise
        """

        if player.handicapped_bid and bid_amount == not_allowed:
            return False
        
        if 0 <= bid_amount < 9:
            player.bid = bid_amount
            self.current_bids[player.name] = bid_amount
            print("SUCC")
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

        total_bids = sum(int(bid) for bid in self.current_bids.values() if bid != 'X')

        return max_cards - total_bids
    

    #testing time !!