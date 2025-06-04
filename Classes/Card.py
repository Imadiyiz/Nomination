# Class script for the cards in the deck


class Card():

    def __init__(self, suit: dict, value: dict):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"