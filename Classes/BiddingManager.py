# Contents for the Bidding Manager python file

from .PlayerClass import Player
from typing import List
import random
from Utils.Tools import clear_screen


class BiddingManager():
    """
    Manages the flow of the bidding logic for players
    """

    def __init__(self, UIManager):
        self.current_bids = dict()
        self.current = 0
        self.not_allowed = -1
        self.current_bids = dict()
        self.UIManager = UIManager

    def update_current_bids(self, player_queue: List[Player]):
        """
        Function for updating the current bids dictionary based on the turn order
        Ideally meant to be used once before the round commenences

        Args:
            player_queue (list[Player]): The player queue is necessary to preserve the correct order
        """

        self.current_bids = {
            player.name: player.bid if player.bid > -1 else 'X'
            for player in player_queue
        }
    
    def successful_player_bid(self, player: Player, not_allowed: int = -1, bid_amount: int = 0) -> bool:
        """
        Validates the player bid

        Returns:
          bool: True if the bid is successful, False otherwise
        """

        if player.handicapped_bid and bid_amount == not_allowed:
            return False
        
        if 0 <= bid_amount < 9:
            player.bid = bid_amount
            self.current_bids[player.name] = bid_amount
            return True
        
        return False

    def reset_bids(self, player_queue: List[Player]):
        for player in player_queue:
            player.reset_bid()
            self.current_bids[player.name] = 'X'
        
    def calculate_banned_number(self, max_cards):
        """
        Function for calculating the banned number the player is unable to bid this round
        """

        total_bids = sum(int(bid) for bid in self.current_bids.values() if bid != 'X')
        banned_number = max_cards - total_bids 
        return banned_number if banned_number > -1 else -1
    
    def computer_bid(self, player_queue: List[Player], player:Player = None, max_cards: int = 8):
        """
        High level block of computer user making a bid

        Returns True when a bid is complete
        Raises error if anything goes wrong
        """
        bid_invalid = True
        not_allowed = self.calculate_banned_number(max_cards)
        while bid_invalid:
            bid  = random.randint(0, max_cards//2) #highest is 3 for the 6 card rounds
            if bid == not_allowed and player.handicapped_bid:
                bid_invalid = True
            else:
                bid_invalid = False


        player.bid = bid
        self.UIManager.display_message(f"{player.name} Bid {player.bid} Card{'s' if player.bid != 1 else '' }")

        self.update_current_bids(player_queue=player_queue)


    def start_bidding(self, trump_suit:str, player_queue: List[Player], round_no:int = 1, max_cards: int = 8):
            """
            Function for the functionality of the bidding round
            """
            clear_screen()
            
            #Bidding output begins
            self.UIManager.display_message(f"""\nBIDDING BEGINS\n""")

            #Loop for every player in the list since order matters
            for _player in player_queue:

                #if human, use the player bid menu
                if _player.computer == False:
                    self.create_player_bid_menu(player_queue=player_queue, player=_player,
                                                round_no = round_no, max_cards=max_cards, trump_suit=trump_suit)
                else:
                    self.computer_bid(player=_player, max_cards=max_cards, player_queue=player_queue)


            #end bidding information
            clear_screen()

            self.display_round_difference(max_cards=max_cards)

            #output current bids
            self.UIManager.display_message(f"CURRENT BIDS: {self.current_bids}\n")

    def display_round_difference(self, max_cards):
                
        """
        Displays the difference between the possible winning hands and the amount bidded by players
        """

        #calculate + or - round
        total_bids = 0
        for bid in self.current_bids.values():
            total_bids += bid
        difference = total_bids-max_cards

        self.UIManager.display_message(f"{'+' if total_bids > max_cards else '-'}{abs(difference)} ROUND")

    def create_player_bid_menu(self, player_queue: List[Player], player:Player = None, 
                               round_no:int = 1, max_cards: int = 8, trump_suit: str = ""):
            """
            Function for creating the player bid menu, ensuring that the computer players do not need the menu
            """
            self.update_current_bids(player_queue)

            bidding_menu = (
f"""{player}'s TURN BIDDING

CURRENT BIDS: {self.current_bids }
TRUMP: {trump_suit.upper()}
HAND: {player.display_hand_str()}

[B] BID\n
""")                
            bid_complete = False
            while not bid_complete and player.computer == False:

                #cleans screen before printing the bidding menu
                clear_screen()
                self.UIManager.display_message(f"""ROUND {round_no}: {max_cards} CARDS PER HAND\n""")
                user_input = self.UIManager.get_player_input((bidding_menu))

                if user_input[0].upper() == 'B':
                        #player gets to enter bid
                            run = True
                            while run:
                                clear_screen()
                                #check for handicap
                                    # apply param if handicapped  
                                if self.player_bid(player_queue=player_queue,
                                    player=player, max_cards=max_cards):
                                    run = False
                                    bid_complete = True
                                else:
                                    self.UIManager.display_message("TRY AGAIN, Unable to bid")
                else:
                            raise Exception("Invalid Menu Option")
                
    def player_bid(self, player_queue: List[Player], player:Player=None, max_cards: int = 8):
        """
        High level block of player making bid, handles validation of input

        Returns TRUE or FALSE based on whether the bid was valid

        Args:
            player (Player): The player instance which is performing the bidding
        """

        #need to calculate handicapped here
        #reorders the dictionary 
        self.update_current_bids(player_queue)
        
        not_allowed = self.calculate_banned_number(max_cards)

        #receive user input
        enter_bid_prompt = (
        f"ENTER BID (BANNED: {not_allowed})\n" if player.handicapped_bid and not_allowed > -1
        else "ENTER BID\n"
        )
        user_input = self.UIManager.get_player_input(enter_bid_prompt)
        self.UIManager.display_message(f"{player} is bidding now")

        #working with input  
        if user_input[0].strip():
            try:
                bid_value = int(user_input[0])
                is_valid = self.successful_player_bid(
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

    #testing time !!