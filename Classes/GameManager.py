# Contents of the GameManager class

from .TableClass import Table
from .DeckClass import Deck
from .PlayerClass import Player
import random
from .ScoreboardClass import Scoreboard
from .UIManager import UIManager
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
        Initialises the game and the objects it requires. 

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
        self.UIManager = UIManager()
        self.table = Table(self.UIManager)
        self.biddingManager = BiddingManager(self.UIManager)
        self.playerStateManager = PlayerStateManager(self.player_set)
        self.trumpManager = TrumpManager(self.UIManager)
        

    def handle_bidding_phase(self):
        """
        Bidding logic
        """

        self.max_cards = self.cards_per_round[self.round-1]
        self.playerStateManager.reset_players_handicap()
        #dealer shifts eveery time bidding starts
        if self.round > 1:
            self.original_queue = self.playerStateManager.update_dealer_order(self.original_queue)
            self.player_queue = self.original_queue
        
        self.player_queue[-1].handicapped_bid = True
        self.biddingManager.reset_bids(self.player_queue)
        self.biddingManager.update_current_bids(self.player_queue)
        self.deck.generate_deck()
        self.deal_cards(amount_to_deal=self.cards_per_round[self.round - 1])

        #starts the bidding process
        self.biddingManager.start_bidding(trump_suit=self.trump_suit,
                                        round_no=self.round, player_queue=self.player_queue,
                                        max_cards=self.max_cards)
        self.phase = "playing"

    def handle_playing_phase(self):
        """
        Playing logic
        """
        cards = self.cards_per_round[self.round-1]
        for _ in range(cards):
            self.start_round()
            self.score_hand()
        self.phase = "scoring"
        if self.round > 1:
            self.trump_suit = self.trumpManager.decide_trump(player_set=self.player_set, current_trump=self.trump_suit)
    
    def handle_scoring_phase(self):
        """
        Scoring logic
        """
        if self.round < 6:
            self.round += 1
            self.phase = "bidding"
            #display total scoreboard
            self.scoreboard.update_total_scoreboard(self.player_queue, max_cards=self.max_cards)
            self.UIManager.display_message(self.scoreboard.display(round=False))
        else:
            self.phase = "game_over"

    def deal_cards(self, amount_to_deal: int = 0):
        """
        Function for dealing cards to the players
        """
        #generates new deck
        self.deck.generate_deck()

        #deal cards for player
        for player in self.player_set:
            player.collect_hand(self.deck.generate_hand(amount=amount_to_deal))

    def start_round(self):
        """
        Function for the functionality of the playing round

        "Remember to shuffle the order of the player list so that the person in first position is now last"
        """
        user_choice = ""
        self.table.reset()
        self.scoreboard.reorder_round_scoreboard(player_queue=self.player_queue)

        for player in self.player_queue:
            run = True
            while run:
                    if player.computer:
                        for card in player.hand:
                            if self.table.valid_add_to_stack(player_hand=player.hand,
                                                            card=card):
                                self.table.add_to_stack(card=card)
                                self.UIManager.display_message(f"{player.name} played a {card}")
                                player.remove_card(card)
                                break
                        run = False
                    else:
                       
                        #logic for selecting a card to add to the stack
                        user_choice  = self.UIManager.get_player_input(
                            self.display_ingame_menu(player))
                        if user_choice[0].isdigit():
                            user_choice = int(user_choice[0])
                            if user_choice <= len(player.hand):
                                if self.table.valid_add_to_stack(card=player.hand[user_choice], 
                                                                player_hand = player.hand):
                                    #if valid then add it to the queue
                                    self.table.add_to_stack(card=player.hand[user_choice])
                                    player.remove_card(card=player.hand[user_choice])
                                    run = False
                            else:
                                self.UIManager.display_message(f"INVALID CARD CHOICE - OPTION MUST BE LESS THAN MAX LENGTH")
                        else:
                            self.UIManager.display_message("INVALID OPTION")


    def score_hand(self):
        """
        Scores on a play by play basis (multiple times per round)
        """

        winner_card = self.table.verify_winner(trump_suit=self.trump_suit)
        winning_player = winner_card.owner
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

I'm going to rework the whole bidding manager setup, so that the bidding manager can handle everything to do with the bidding

"""