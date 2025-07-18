# Contents of the GameManager class

from .TableClass import Table
from .DeckClass import Deck
from .PlayerClass import Player
from .CardClass import Card
import random
from .ScoreboardClass import Scoreboard
from .UIManager import UIManager
from Utils.tools import clear_screen
from .BiddingManager import BiddingManager
from .PlayerStateManager import PlayerStateManager
from .TrumpManager import TrumpManager

class Game():
    """
    Class for managing the game state and orchestrating the gamee

    Attributes:
        player_queue (list): A list which stores the order of which the players are playing
        menu_options (dict): A dictionary which stores the current options for the menu
        round (int): An integer value of the current round the game is in
        cards_per_round (list): A ;ist of the maximum cards per round
        phase (str): A string which indicates the current action of the game object
    """

    def __init__(self,*args, **kwargs):
        """
        When initialised, the game object should receive the player parameters
        """
        self.menu_options = {
            "S": "SHOW HAND",
            "B": "BID" 
        }

        self.round = 1
        self.cards_per_round = [8,7,6,6,7,8]
        self.phases = {
            "bidding": self.handle_bidding_phase,
            "playing": self.handle_playing_phase,
            "scoring": self.handle_scoring_phase,
        }
        self.phase = "bidding"

        #creates a temp list with the player objects in
        temp_list = []
        temp_set = set()
        for List in args:
            for player in List:
                temp_list.append(player)

        self.player_set = set()
        self.player_queue = temp_list #queue for playing during rounds
        self.original_queue = temp_list #queue for after round when winning the hand does not affect the order

        ##
        #reset players and remove duplicate names
        names_dict = {}
        count = 2
        for player in self.player_queue:
            if player.name not in names_dict:
                names_dict[player.name] = 1
                self.player_set.add(player)
            else:
                player.name += str(count)
                names_dict[player.name] = count
                self.player_set.add(player)
                count +=1

        #places the shuffled players into the actual list in their new order
        random.shuffle(self.player_queue)
        
        if len(self.player_set) > 6:
            raise Exception("Too many players in the game")
        if len(self.player_set) < 3:
            raise Exception("Not enough players in the game")

    def create_game(self):
        """
        Function for creating the initial game. 

        """        
        #generate deck
        self.deck = Deck()
        
        #determine trump
        #since deck is already shuffled, should be ok to pick first card
        self.trump_suit = self.deck.deck[0].suit[0]
        print("\nDECIDING INITIAL TRUMP")
        print("CARD RANDOMLY CHOSEN:: ", self.deck.deck[0])
        print("TRUMP SUIT:: ", self.trump_suit, "\n")

        #Generates objects for the game
        self.scoreboard = Scoreboard(self.player_set)
        self.table = Table(max_players=len(self.player_set))
        self.UIManager = UIManager()
        self.biddingManager = BiddingManager(self.player_set)
        self.playerStateManager = PlayerStateManager(self.player_set)
        self.trumpManager = TrumpManager(self.UIManager)
        

    def handle_bidding_phase(self):
        """
        Cards are dealt for players, and reset
        """

        self.playerStateManager.reset_players_handicap()
        #dealer shifts eveery time bidding starts
        if self.round > 1:
            self.original_queue = self.playerStateManager.update_dealer_order(self.original_queue)
            self.player_queue = self.original_queue
        
        self.player_queue[-1].handicapped_bid = True
        self.biddingManager.reset_bids()
        self.deck.generate_deck()
        self.deal_cards(amount_to_deal=self.cards_per_round[self.round - 1])

        #starts the bidding process
        self.start_bidding(round_no=self.round)
        self.phase = "playing"

    def handle_playing_phase(self):
        """
        """
        cards = self.cards_per_round[self.round-1]
        for _ in range(cards):
            self.start_round()
            self.score_round()
        self.phase = "scoring"
        if self.round > 1:
            self.trump_suit = self.trumpManager.decide_trump()
    
    def handle_scoring_phase(self):
        """
        Scoring logic
        """
        #self.score_round()
        if self.round < 6:
            self.round += 1
            self.phase = "bidding"
        else:
            self.phase = "game_over"
        

    def player_bid(self, player:Player=None):
        """
        High level block of player making bid, handles validation of input

        Returns TRUE or FALSE based on whether the bid was valid

        Args:
            player (Player): The player instance which is performing the bidding
        """

        #reorders the dictionary 
        self.biddingManager.reorder_current_bids(self.player_queue)
        _max_cards = self.cards_per_round[self.round-1]
        
        not_allowed = self.biddingManager.calculate_banned_number(_max_cards)
        #check for handicap

        enter_bid_prompt = (
        f"ENTER BID (BANNED: {not_allowed})\n" if player.handicapped_bid
        else "ENTER BID\n"
        )
        user_input = self.UIManager.get_player_input(enter_bid_prompt)

        #handicapped check
        for player in self.player_queue:
            if player.handicapped_bid:
                print(player.name, player.handicapped_bid)

        #working with input  
        if user_input[0].strip():
            try:
                bid_value = int(user_input[0])
                is_valid = self.biddingManager.successful_player_bid(
                    player, not_allowed=not_allowed, bid_amount=bid_value
                )
                if is_valid:
                    msg = f"{player.name} bid {bid_value} Card" + ("s" if bid_value != 1 else "")
                    self.UIManager.display_message(msg)
                    return True
                else:
                    self.UIManager.display_message("Unable to bid that amount.")
            except ValueError:
                self.UIManager.display_message("Invalid input. Enter a number.")
        return False
                
    def create_player_bid_menu(self, player:Player = None, round_no:int = 1):
            """
            Function for creating the player bid menu, ensuring that the computer players do not need the menu
            """
            _max_cards = self.cards_per_round[self.round - 1]
            self.biddingManager.reorder_current_bids(self.player_queue)
            _current_bids = self.biddingManager.current_bids
            self.menu_options = {
                        'B': 'BID'
                        }
            menu_options_string = self.create_menu_options_string()

            bidding_menu = (
f"""{player}'s TURN BIDDING

CURRENT BIDS: {_current_bids }
TRUMP: {self.trump_suit.upper()}
HAND: {player.display_hand_str()}

{menu_options_string}
""")                
            bid_complete = False
            while not bid_complete and player.computer == False:

                #cleans screen before printing the bidding menu
                clear_screen()
                print(f"""ROUND {round_no}: {_max_cards} CARDS PER HAND\n""")
                user_input = self.UIManager.get_player_input((bidding_menu))

                if user_input[0].upper() in self.menu_options:
                        if user_input[0].upper() == "S":
                            #Show Hand
                            clear_screen()
                            self.menu_options = {
                        'B': 'BID'
                        }
                            #updates the bidding options
                            menu_options_string = self.create_menu_options_string()
                            
                        elif user_input[0].upper() == 'B':
                        #player gets to enter bid
                            run = True
                            while run:
                                clear_screen()
                                #check for handicap
                                if player.handicapped_bid:
                                    # apply param if handicapped  
                                    if self.player_bid(player=player):
                                        run = False
                                        bid_complete = True
                                else:
                                    if self.player_bid(player=player):
                                        run = False
                                        bid_complete = True
                                    else:
                                        self.UIManager.display_message("TRY AGAIN")

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
        if bid == 1:
            self.UIManager.display_message(f"{player.name} Bid 1 Card")
        else:
            self.UIManager.display_message(f"{player.name} Bid {player.bid} Cards")

        self.biddingManager.update_current_bids()
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
        #generates new deck
        self.deck.generate_deck()

        #deal cards for player
        for player in self.player_set:
            player.collect_hand(self.deck.generate_hand(amount=amount_to_deal))

    def start_bidding(self, round_no:int = 1):
        """
        Function for the functionality of the bidding round
        """
        clear_screen()
        self.phase = "bidding"
        _max_cards = self.cards_per_round[self.round - 1]
        
        #Bidding output begins
        print(f"""\nBIDDING BEGINS\n""")

        #Loop for every player in the list since order matters
        for player in self.player_queue:

            #if human, use the player bid menu
            if player.computer == False:
                self.create_player_bid_menu(player, round_no = round_no)
            else:
                 #check for handicap
                if player.handicapped_bid:
                    banned = self.biddingManager.calculate_banned_number(max_cards=_max_cards)     
                    # apply param if handicapped  
                    self.computer_bid(player=player, not_allowed=banned)
                else:
                    self.computer_bid(player)

        #end bidding information
        clear_screen()

        #output current bids
        print(f"CURRENT BIDS: {self.biddingManager.current_bids}\n") #may need updating beforehand
        print("ERROR HERE")
        for player in self.player_queue:
            print(player.bid, player.name, player.handicapped_bid)

        #calculate + or - round
        total_bids = 0
        for bid in self.biddingManager.current_bids.values():
            total_bids += bid
        if total_bids > _max_cards:
            print(f"+{total_bids-_max_cards} ROUND")
        else:
            print(f"-{_max_cards-total_bids} ROUND")

    def start_round(self):
        """
        Function for the functionality of the playing round

        "Remember to shuffle the order of the player list so that the person in first position is now last"
        """
        user_choice = ""
        self.table.reset()
        self.scoreboard.reorder_round_scoreboard(player_queue=self.player_queue)

        for player in self.player_queue:
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
                            if self.table.valid_add_to_stack(card=player.hand[user_choice], trump_suit=self.trump_suit, first_card=first_card, player_hand = player.hand):
                                #if valid then add it to the queue
                                self.table.add_to_stack(card=player.hand[user_choice])
                                player.remove_card(card=player.hand[user_choice])
                                run = False
                            else:
                                self.UIManager.display_message(f"INVALID CARD CHOICE - WRONG SUIT: MUST BE {first_card.suit[0]}")
                        else:
                            self.UIManager.display_message(f"INVALID CARD CHOICE - OPTION MUST BE LESS THAN MAX LENGTH")
                    else:
                        self.UIManager.display_message("INVALID OPTION")


    def score_round(self):
        """
        Function for scoring on a play by play basis (multiple times per round)
        """

        winner_card = self.table.verify_winner(trump_suit=self.trump_suit)
        winning_player= winner_card.owner
        self.UIManager.display_message(message=f"DONE, {winning_player} is the winner with {winner_card}")
        self.scoreboard.update_round_scoreboard(self.player_set, winner_card=winner_card)
        self.player_queue = self.playerStateManager.update_winner_order(winner=winning_player, player_queue=self.player_queue)

    def display_ingame_menu(self, player:Player) -> str:
        """
        Displays the menu for the player during the round

        The menu includes:
        PLAY_cARD, 
        """
        round_scoreboard = self.scoreboard.display()
        hand_str = player.display_hand_str()
        stack_str = self.table.display_stack()
        _string = f"""
{player.name} STARTS PLAYING

ROUND SCOREBOARD{round_scoreboard}
TRUMP: {self.trump_suit}
HAND:\n {hand_str}
STACK: {stack_str}
ENTER THE INDEX VALUE OF THE CARD YOU WANT TO PLAY
INPUT RANGE: {0}-{len(player.hand)-1}\n"""
        return _string
    
""" TODO: 


12/07/25
UNABLE TO BID FREELY ON SECOND ROUND 

13/07/25
DEALER SWITCHES AFTER EACH ROUND
I AM CURRENTLY BIDDING FOR THE FOR THE AI AT THE MOMENT LEAVING THE PLAYER WITHOUT THEIR OWN BID

18/07/2025
i AM STRUGGLING SINCE THE BIDDING VALUES OF THE HUMANS ARE NOT SAVING OR ARE BEING RESET i WILL FIND OUT,
THE TODAY i WILL WRITE LOTS OF UNIT TESTS TO GET BETTER AT THEM

"""