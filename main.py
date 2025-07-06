# contents of the game loop

from Classes.GameManager import Game
from Classes.PlayerClass import Player

from Utils.tools import clear_screen

#define the max_cards per round in a list
cards_per_round = [8,7,6,6,7,8]


def setup_game():
        """
        Function for setting up the game with the settings
        """
        #v = validate
        no_of_players = int(input("ENTER TOTAL AMOUNT OF PLAYERS (MAX 6)")[0])
        print(f"{no_of_players} Players selected")

        player_dict = {}

        for x in range(no_of_players):
            player_name = str(input(f"ENTER NAME FOR PLAYER {x + 1}\t"))
            bot_boolean = str(input("IS THIS PLAYER A HUMAN? (Y/N)\t"))
            if bot_boolean[0].lower() == 'y':
                player_dict[player_name] = False
            else:
                player_dict[player_name] = True

        player_list = []
        for key,value in player_dict.items():
            player = Player(name=key, computer=value)
            player_list.append(player)            

        game = Game(player_list)
        game.create_game()

        return game

game = setup_game()
clear_screen(1) #5
# At this point the bidding is complete
"""0,8 """
for round, value in enumerate(cards_per_round):  
    game.start_bidding(max_cards=value, round_no=round+1) 
    game.start_round(max_cards=round)

#my_game.scoreboard.update_total_scoreboard(my_game.player_list)


#gameloop
while True:
    pass