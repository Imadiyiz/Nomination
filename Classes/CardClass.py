# Class script for the cards in the deck

class Card():

    def __init__(self, suit: tuple, value: tuple, owner: 'Player' = None): # Forward reference to avoid nameError
        self.suit = suit
        self.value = value
        self.owner = owner
        self.picture = self.generate_picture()

    def __str__(self):
        return f"{self.value[0]} {self.suit[0]}"
    
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