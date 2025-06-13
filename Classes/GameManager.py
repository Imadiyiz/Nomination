# Contents of the GameManager class

from .TableClass import Table
from .DeckClass import Deck
from .PlayerClass import Player
from .CardClass import Card
import random
from queue import Queue
from .ScoreboardClass import Scoreboard
from Utils.tools import clear_screen

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
        self.current_bids = {}
        self.menu_options = {
            "S": "SHOW HAND",
            "B": "BID" 
        }

        #creates a temp list with the player objects in
        temp_list = []
        for List in args:
            for player in List:
                temp_list.append(player)

        self.player_list = temp_list

        #reset players and remove duplicate names
        names_dict = {}
        for player in self.player_list:
            player.reset_dealer_trump_decider()
            if player.name not in names_dict:
                names_dict[player.name] = 1
            else:
                player.name = f"{player.name}{names_dict[player.name]+1}"
                names_dict[player.name] = 1

        #places the shuffled players into the actual queue in their new order
        random.shuffle(temp_list)
        for player in self.player_list:
            self.player_queue.put(player)
        
        if self.player_queue.qsize() > 6:
            raise Exception("Too many players in the game")
        if self.player_queue.qsize() < 2:
            raise Exception("Not enough players in the game")
        
        #Creates a dictionary which contains the current bidding amounts per player
        for player in self.player_list:
            self.current_bids[player.name] = 'X'

    def update_current_bids(self):
        """
        Function for updating the current bids scoreboard ensuring it stays in sync
        """

        for player in self.player_list:
            if player.bid > -1:
                self.current_bids[player.name] = player.bid

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
        print("\nDECIDING INITIAL TRUMP")
        print("CARD RANDOMLY CHOSEN:: ", self.deck.deck[0])
        print("TRUMP SUIT:: ", self.trump_suit, "\n")

        #Generate scoreboard object, table object and message_queue object
        self.scoreboard = Scoreboard(self.player_list)
        self.table = Table(max_players=self.player_queue.qsize())
        
    def player_bid(self, player:Player=None, not_allowed:int = -1):
        """
        High level block of player making bid

        Returns True if success
        Returns False if bid is invalid
        """
        if not_allowed >= 0:
            user_input = input(f"ENTER BID (BANNED: {not_allowed})\n")
        else:
            user_input = input("ENTER BID\n")
        if int(user_input[0]):
                user_input = int(user_input[0])
                if user_input == not_allowed:
                    print(f"Unable to bid that amount")
                    return False
                if user_input < 9:
                    player.bid = user_input
                    self.current_bids[player.name] = player.bid
                    self.update_current_bids()
                    if user_input == 1:
                        print(f"{player.name} Bid 1 Card")
                    else:
                        print(f"{player.name} Bid {player.bid} Cards")
                    return True

    def create_menu_options_string(self):
        """
        Function for creating the menu options string to ensure it is up to date
        """
        menu_options_string = ""
        for char, option in self.menu_options.items():
                    menu_options_string += f"[{char}] {option}\n"

        return menu_options_string

        
    def deal_cards(self, amount_to_deal: int = 0):
        """
        Function for dealing cards to the players
        """
        #deal cards for player
        for _ in range(self.player_queue.qsize()):
            temp_player = self.player_queue.get()
            temp_player.collect_hand(self.deck.generate_hand(amount=amount_to_deal))
            self.player_queue.put(temp_player)

    def start_bidding(self, max_cards):
        """
        Function for the functionality of the bidding round
        """

        clear_screen()
        self.game_state = "BIDDING START"

        #last person has a handicapped bid
        self.player_list[-1].handicapped_bid = True
        
        print(f"""\nBIDDING BEGINS\n""")

        #Loop for every player in the list
        for player in self.player_list:
            player.reset_bid()            

            self.menu_options = {
                        'S': 'SHOW HAND',
                        'B': 'BID'
                        }
            menu_options_string = self.create_menu_options_string()

            bidding_menu = (
f"""{player}'s TURN BIDDING

CURRENT BIDS: {self.current_bids}
TRUMP: {self.trump_suit.upper()}
HAND: {player.hidden_hand}

{menu_options_string}
""")                
            bid_complete = False
            while not bid_complete:
            #cleans screen before printing the bidding menu
                clear_screen()
                user_input = input((bidding_menu))

                if user_input[0].upper() in self.menu_options:
                        if user_input[0].upper() == "S":
                            #Show Hand
                            clear_screen()

                            self.menu_options = {
                        'B': 'BID'
                        }
                            menu_options_string = self.create_menu_options_string()
                            bidding_menu = (
f"""{player}'s TURN BIDDING

CURRENT BIDS: {self.current_bids}
TRUMP: {self.trump_suit.upper()}
HAND: {player.display_hand()}

{menu_options_string}
""")
                        elif user_input[0].upper() == 'B':
                        #player gets to enter bid
                            run = True
                            while run:
                                clear_screen()
                                #check for handicap
                                if player.handicapped_bid:
                                    banned = int()
                                    #calculate banned number
                                    for number in self.current_bids.values():
                                        if number != 'X':
                                            banned += int(number)
                                    banned = max_cards - banned       
                                    # apply param if handicapped                                 
                                    if self.player_bid(player=player, not_allowed=banned) == True:
                                        run = False
                                        bid_complete = True
                                else:
                                    if self.player_bid(player=player) == True:
                                        run = False
                                        bid_complete = True
                                    else:
                                        print("TRY AGAIN")



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
        print(self.display_ingame_menu())
        #print(self.message_queue.output_queue())
        #self.table

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
    
""" TODO: Need to fix the logic with the show hand. I should just show the hand and then play the 
game instead of hiding it and unhiding it. 


"""