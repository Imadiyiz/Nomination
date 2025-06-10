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
        self.player_queue = Queue()

        #creates a temp list with the player objects in
        temp_list = []
        for player in args:
            temp_list.append(player)

        #reset players and remove duplicate names
        names_dict = {}
        for player in temp_list:
            player.reset_dealer_trump_decider()
            if player.name not in names_dict:
                names_dict[player.name] = 1
            else:
                player.name = f"{player.name}{names_dict[player.name]+1}"
                names_dict[player.name] = 1

        #places the shuffled players into the actual queue in their new order
        random.shuffle(temp_list)
        for player in temp_list:
            self.player_queue.put(player)
        
        if self.player_queue.qsize() > 6:
            raise Exception("Too many players in the game")
        


    def create_game(self):
        """
        Function for creating the initial game.

        Must define the amount of players in the game

        #Players should have been initialised beforehand
        """
        self.game_state = "CREATE_GAME"
        
        #set dealer
        first_player = self.player_queue.get()
        first_player.set_dealer()
        self.player_queue.put(first_player)
        
        #generate deck
        self.deck = Deck()

        #deal cards
        self.deal_cards(amount_to_deal=8)
        
        #determine trump
        #since deck is already shuffled, should be ok to pick first card
        trump_suit = self.deck.deck[0].suit[0]
        print("CARD RANDOMLY CHOSEN:: ", self.deck.deck[0])
        print("TRUMP SUIT:: ", trump_suit)

        #generate list for Scoreboard class
        player_list = self.create_player_list()

        #Generate scoreboard object and table object
        self.scoreboard = Scoreboard(player_list)
        self.table = Table(max_players=self.player_queue.qsize())

    def deal_cards(self, amount_to_deal: int = 0):
        """
        Function for dealing cards to the players
        """
        #deal cards for player
        for _ in range(self.player_queue.qsize()):
            temp_player = self.player_queue.get()
            temp_player.collect_hand(self.deck.generate_hand(amount=amount_to_deal))
            self.player_queue.put(temp_player)

    def create_player_list(self):
        """
        Function for creating a player_list
        """
        player_list = []
        for _ in range(self.player_queue.qsize()):
            temp_player = self.player_queue.get()
            player_list.append(temp_player)
            self.player_queue.put(temp_player)
        return player_list

    def start_bidding(self, max_cards):
        """
        Function for the functionality of the bidding round
        """

        for player in self.create_player_list():
            player.reset_bid()

