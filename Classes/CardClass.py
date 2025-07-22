# Class script for the cards in the deck

class Card():

    """
    Represents a playing card with a suit, value, and optional owner.

    Each card has a suit (e.g., "Heart", "♦"), a value (e.g., "10", 10),
    and can optionally have an owner (a Player object). Upon creation,
    the card generates an ASCII representation of itself.

    Attributes:
        suit (tuple): The suit of the card, e.g., ("Heart", "♥").
        value (tuple): The value of the card, e.g., ("10", 10) or ("Ace", 14).
        owner (Player, optional): The owner of the card.
        picture (str): The ASCII representation of the card.

    Methods:
        generate_picture():
            Generates and returns an ASCII representation of the card.

        __eq__(other):
            Checks equality between two Card objects based on suit and value.

        __str__():
            Returns a string representation of the card (e.g., "10 Heart").

        __hash__():
            Returns a hash value for the card, allowing it to be used in sets and dictionaries.
    """

    def __init__(self, suit: tuple, value: tuple, owner: 'Player' = None): # Forward reference to avoid nameError
        self.suit = suit
        self.value = value
        self.owner = owner
        self.picture = self.generate_picture()
    
    def generate_picture(self):
        """
        Function for creating a string picture of the card
        """
        self.picture=""
        if self.value[1] == 10:
            self.picture = f"""
                            _________
                            |{self.value[0]}     |
                            |       |
                            |   {self.suit[1]}   |
                            |       |
                            |     {self.value[0]}|
                            |-------|
                            """
        elif self.value[1] < 10:
            self.picture = f"""
                            _________
                            | {self.value[0]}     |
                            |       |
                            |   {self.suit[1]}   |
                            |       |
                            |     {self.value[0]} |
                            |-------|
                            """
        elif self.value[0] == "King":
            self.picture = f"""
                            _________
                            | {self.suit[1]}     |
                            |       |
                            |  {self.value[0]} |
                            |       |
                            |     {self.suit[1]} |
                            |-------|
                            """
        elif self.value[0] == "Queen":
            self.picture = f"""
                            _________
                            | {self.suit[1]}     |
                            |       |
                            | {self.value[0]} |
                            |       |
                            |     {self.suit[1]} |
                            |-------|
                            """
        elif self.value[0] == "Jack":
            self.picture = f"""
                            _________
                            | {self.suit[1]}     |
                            |       |
                            |  {self.value[0]} |
                            |       |
                            |     {self.suit[1]} |
                            |-------|
                            """
        elif self.value[0] == "Ace":
            self.picture = f"""
                            _________
                            | {self.suit[1]}     |
                            |       |
                            |  {self.value[0]}  |
                            |       |
                            |     {self.suit[1]} |
                            |-------|
                            """
        # Returns the picture string
        if self.picture:
            return self.picture
        return None
    
    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value
    
    def __str__(self):
        return f"{self.value[0]} {self.suit[0]}"
    
    def __hash__(self):
        return hash(str(self))