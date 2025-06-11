# contents of the game loop

from Classes.GameManager import Game
from Classes.PlayerClass import Player

def setup_game():
        """
        Function for setting up the game with the settings
        """
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


setup_game()

#gameloop
while True:
    pass