# Contents of the GameManager class

from .TableClass import Table
from .DeckClass import Deck
from .PlayerClass import Player
from .CardClass import Card
import random
from queue import Queue
from .ScoreboardClass import Scoreboard
from .MessageManager import MessageQueue

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
        self.player_list = self.create_player_list()

        #creates a temp list with the player objects in
        temp_list = []
        for listr in args:
            for player in listr:
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
        self.trump_suit = self.deck.deck[0].suit[0]
        print("CARD RANDOMLY CHOSEN:: ", self.deck.deck[0])
        print("TRUMP SUIT:: ", self.trump_suit)

        #Generate scoreboard object, table object and message_queue object
        self.scoreboard = Scoreboard(self.player_list)
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
        self.game_state = "BIDDING START"
        for player in self.player_list:
            player.reset_bid()
        
        self.message_queue.add_to_queue(f"""
                                        BIDDING BEGINS\n
                                        {self.player_list[0]} BIDDING FIRST""")
        
        print(self.message_queue.output_queue())

    def end_bidding(self):
        """
        Function for ending the bidding round
        """

        self.game_state = "BIDDING END"

    def start_playing(self):
        """
        Function for the functionality of the playing round
        """

        self.game_state = "PLAYING START"
        self.message_queue.add_to_queue(self.display_ingame_menu())
        print(self.message_queue.output_queue())
        #self.table

    def player_bid(self, player:Player):
        """
        Function for the functionality of the player's individual bid during the round

        Holds inforamtion about the bid, the message and the player
        """

        bid = input("Type the number of the cards you want to bid")

    def display_ingame_menu(self, player:Player):
        """
        Displays the menu for the player during the round

        The menu includes:
        VIEW_SCOREBOARD, VIEW STACK, 
        """
        round_scoreboard = self.scoreboard.display()
        string = f"""
        {player.name} STARTS PLAYING

        ROUND SCOREBOARD{round_scoreboard}
        TRUMP: {self.trump_suit}
        HAND: {player.show_hand()}
        STACK: {self.table.stack}

        [1] SHOW HAND 
        [2] VIEW OVERALL SCOREBOARD
        [3] PLAY CARD
        [9] EXIT        
        """

        return string