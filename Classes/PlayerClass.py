# Contents of the Player class python file

from .CardClass import Card
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Player:
    """
    Handles the hand functionality of players.
    Players are able to collect hands and play cards.
    
    """
    name: str = "AI"
    hand: List[Card] = field(default_factory=list) #each player gets their own hand list
    total_score: int = 0
    round_score: int = 0
    bid: int = -1 # must be -1 because 0 is a valid bid
    trump_decider:bool = False
    dealer:bool = False
    computer: bool = True,
    handicapped_bid:bool = False

    def collect_hand(self, hand: List[Card]):
        for card in hand:
            card.owner = self
        self.hand = hand

    def remove_card(self, card: Card):
        for _card in self.hand:
            if card == _card:
                self.hand.remove(_card)
                return

    def find_card(self, selected_suit: str, selected_value: str) -> bool:
        for card in self.hand:
            if card.suit[0].lower() == selected_suit.lower() and card.value[0].lower() == selected_value.lower():
                return True
        return False

##
    def set_trump_decider(self, boolean: bool):
        self.trump_decider = boolean

##
    def set_dealer(self):
        self.dealer = True

    def reset(self):
        self.bid = -1
        self.dealer = False
        self.trump_decider = False
        self.handicapped_bid = False    
        self.hand = []    
    
    ##
    def display_hand_str(self) -> str:
        hand_str = ""
        for card in self.hand:
            hand_str += f"{card}\n"

        return hand_str

    def reset_bid(self):
        self.bid = -1

    def __str__(self):
        return self.name