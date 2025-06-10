# Contents of the GameManager class

from TableClass import Table
from DeckClass import Deck
from PlayerClass import Player
from CardClass import Card
import random
from queue import Queue
from ScoreboardClass import Scoreboard

class Game():
    """
    Class for managing the game state and events in the game.

    Used for a high level understanding of how the game should run
    """

    def __init__(self,*args, **kwargs):
        """
        When initialised, the game object should receive the player parameters
        """
        self.game_state = None
        self.player_list = Queue()
        #creates a list with the player objects in
        for player in args:
            self.player_list.append(player)

    def create_game(self):
        """
        Function for creating the initial game.

        Must define the amount of players in the game

        #Players should have been initialised beforehand
        """
        self.game_state = "CREATE_GAME"

        #randomise players
        random.shuffle(self.player_list)

        #reset players
        for player in self.player_list:
            player.reset_dealer_trump_decider()

        #set dealer
        self.player_list[0].set_dealer()

        #generate deck
        the_deck = Deck()

        #deal cards for player
        for player in self.player_list:
            player.collect_hand(the_deck.generate_hand())
        
        #determine trump
        #since deck is already shuffled, should be ok to pick first card
        trump_suit = the_deck.deck[0].suit[0]
        print("TRUMP SUIT:: ", trump_suit)

        #generate more objects
        the_scoreboard = Scoreboard(self.playerlist)