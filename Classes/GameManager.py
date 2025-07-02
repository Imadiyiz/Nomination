# Contents of the GameManager class

from .TableClass import Table
from .DeckClass import Deck
from .PlayerClass import Player
from .CardClass import Card
import random
from .ScoreboardClass import Scoreboard
from Utils.tools import clear_screen

class Game():
    """
    Class for managing the game state and event flows in the game.

    Used for a high level understanding of how the game should run, including managing player bidding,
    and menu interactions

    Attributes:
        game_state (str): Stores the current state of the game
        player_queue (list): A list which stores the order of which the players are playing
        current_bids (dict): A dictionary which stores the values of the current bids along with the player
        menu_options (dict): A dictionary which stores the current options for the menu
    """

    def __init__(self,*args, **kwargs):
        """
        When initialised, the game object should receive the player parameters
        """
        self.game_state = None
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

        #places the shuffled players into the actual list in their new order
        random.shuffle(self.player_list)
        
        if len(self.player_list) > 6:
            raise Exception("Too many players in the game")
        if len(self.player_list) < 3:
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

        """
        self.game_state = "CREATE_GAME"
        
        #set dealer
        first_player = self.player_list[0]
        first_player.set_dealer()
        
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

        #Generate scoreboard object, table object 
        self.scoreboard = Scoreboard(self.player_list)
        self.table = Table(max_players=len(self.player_list))

    def calculate_banned_number(self, max_cards):
        """
        Function for calculating the banned number the player is unable to bid this round
        """

        banned = int()
        #calculate banned number
        for number in self.current_bids.values():
            if number != 'X':
                banned += int(number)
        banned = max_cards - banned  

        return banned
        
    def player_bid(self, player:Player=None, not_allowed:int = -1):
        """
        High level block of player making bid

        Args:
            player (Player): The player instance which is performing the bidding
        """
        if not_allowed >= 0:
            user_input = input(f"ENTER BID (BANNED: {not_allowed})\n")
        else:
            user_input = input("ENTER BID\n")
        if user_input[0].strip():
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
                
    def create_player_bid_menu(self, player:Player = None, max_cards:int = None, round_no:int = 1):
            """
            Function for creating the player bid menu, ensuring that the computer players do not need the menu
            """

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
            while not bid_complete and player.computer == False:

                #cleans screen before printing the bidding menu
                clear_screen()
                print(f"""ROUND {round_no}: {max_cards} CARDS PER HAND\n""")
                user_input = input((bidding_menu))

                if user_input[0].upper() in self.menu_options:
                        if user_input[0].upper() == "S":
                            #Show Hand
                            clear_screen()
                            self.menu_options = {
                        'B': 'BID'
                        }
                            #updates the bidding options
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
                                    banned = self.calculate_banned_number(max_cards=max_cards)     
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

    def computer_bid(self, player:Player = None, not_allowed:int = -1):
        """
        High level block of computer user making a bid

        Returns True when a bid is complete
        Raises error if anything goes wrong
        """
        #generate random bid
        bid_invalid = True
        while bid_invalid:
            bid  = random.randint(0,4)
            if bid != not_allowed:
                bid_invalid = False


        player.bid = bid
        self.current_bids[player.name] = player.bid
        self.update_current_bids()
        if bid == 1:
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
        for player in self.player_list:
            player.collect_hand(self.deck.generate_hand(amount=amount_to_deal))

    def start_bidding(self, max_cards, round_no:int = 1):
        """
        Function for the functionality of the bidding round
        """
        clear_screen()
        self.game_state = "BIDDING START"

        #last person has a handicapped bid
        self.player_list[-1].handicapped_bid = True
        
        #Bidding output begins
        print(f"""\nBIDDING BEGINS\n""")

        #Loop for every player in the list
        for player in self.player_list:
            player.reset_bid() 

            #if human, use the player bid menu
            if player.computer == False:
                self.create_player_bid_menu(player, max_cards=max_cards, round_no = round_no)
            else:
                 #check for handicap
                if player.handicapped_bid:
                    banned = self.calculate_banned_number(max_cards=max_cards)     
                    # apply param if handicapped  
                    self.computer_bid(player=player, not_allowed=banned)
                else:
                    self.computer_bid(player)

        #end bidding information
        clear_screen()
        print(f"{self.current_bids}\n")

        #calculate + or - round
        total_bids = 0
        for bid in self.current_bids.values():
            total_bids += bid
        if total_bids > max_cards:
            print(f"+{total_bids-max_cards} ROUND")
        else:
            print(f"-{max_cards-total_bids} ROUND")


    def end_bidding(self):
        """
        Function for ending the bidding round
        """
        self.game_state = "BIDDING END"

    def start_round(self, max_cards):
        """
        Function for the functionality of the playing round

        "Remember to shuffle the order of the player list so that the person in first position is now last"
        """
        user_choice = ""
        self.game_state = "PLAYING START"

        for player in self.player_list:
            first_card = None
            run = True
            while run:
                if player.computer:
                    #if the stack is not empty
                    if self.table.stack:
                        first_card = self.table.stack[0] #gets the bottom item in stack cause error
                    else:
                        first_card = None

                    for card in player.hand:
                        if self.table.valid_add_to_stack(trump_suit=self.trump_suit, card=card, first_card=first_card):
                            self.table.add_to_stack(card=card)
                            print(f"{player.name} played a {card}")
                            player.remove_card(card)
                            break
                    run = False
                else:
                    #logic for selecting a card to add to the stack
                    user_choice  = input(self.display_ingame_menu(player))
                    if user_choice[0].isdigit():
                        user_choice = int(user_choice[0])
                        if user_choice <= len(player.hand):
                            #if the stack is not empty
                            if self.table.stack:
                                first_card = self.table.stack[0] #gets the first card in stack
                                print("FIRST CARD, ", first_card)
                            if self.table.valid_add_to_stack(card=player.hand[user_choice], trump_suit=self.trump_suit, first_card=first_card):
                                #if valid then add it to the queue
                                self.table.add_to_stack(card=player.hand[user_choice])
                                player.remove_card(card=player.hand[user_choice])
                                run = False
                            else:
                                print(f"INVALID CARD CHOICE - WRONG SUIT: MUST BE {self.trump_suit} or {first_card.suit[0]}")
                        else:
                            print(f"INVALID CARD CHOICE - OPTION MUST BE LESS THAN MAX LENGTH")
                    else:
                        print("INVALID OPTION")

        print("Done")


    def decide_trump(self, player:Player):
        """Function for determining the trump for the next round
        Useful for the subsequent rounds of the game"""

        self.trump_suit = ""
        valid_menu_options = ["C", "S", "H", "D"]
        trump_choice = input(
            F"""ENTER YOUR CHOICE OF TRUMP
                [C] CLUB
                [S] SPADE
                [H] HEART
                [D] DIAMOND 
                """).strip()
        
        if trump_choice.upper()[0] in valid_menu_options:
            if trump_choice == "C":
                self.trump_suit = 'club'
            if trump_choice == "S":
                self.trump_suit = 'spade'
            if trump_choice == "H":
                self.trump_suit = 'heart'
            if trump_choice == "D":
                self.trump_suit = 'diamond'



    def display_ingame_menu(self, player:Player) -> str:
        """
        Displays the menu for the player during the round

        The menu includes:
        PLAY_cARD, 
        """
        round_scoreboard = self.scoreboard.display()
        player.show_hand = True #Forces hand to be able to be seen
        hand_str = player.display_hand()
        stack_str = self.table.display_stack()
        _string = f"""
{player.name} STARTS PLAYING

ROUND SCOREBOARD{round_scoreboard}
TRUMP: {self.trump_suit}
HAND:\n {hand_str}
STACK: {stack_str}

ENTER THE INDEX VALUE OF THE CARD YOU WANT TO PLAY
E.G (Enter "0" for '{player.hand[0]}')
MAX VALUE: {len(player.hand)-1}\n"""
        return _string
    
""" TODO: Need to fix the logic with the show hand. I should just show the hand and then play the 
game instead of hiding it and unhiding it. DONE 16/05/25

Returned to this code 25/06/2025 after a small hiatus (I was working and got complacent with progress)

The classes in general are not specific enough (they have multiple uses) and this makes them difficult to test and understand.
I have made some impressive progress in the gaming journey however, I am ready to move onto the new game and make it good.
"""