# contents of the game loop

from Classes.GameManager import Game
from Classes.PlayerClass import Player


def setup_game():
        """
        Function for setting up the game with appropriate 
        amount of players
        """
        #v = validate
        no_of_players = int(input("ENTER TOTAL AMOUNT OF PLAYERS (MAX 6)")[0])
        print(f"{no_of_players} Players selected")

        # Initialise the player dictionary, determining whether a player is computer
        computer_player_dict = {}
        names_count = {}

        for x in range(no_of_players):
            player_name = str(input(f"ENTER NAME FOR PLAYER {x + 1}\t"))
            player_name = player_name.lower()
            
            #validation to avoid duplicate names
            if player_name not in names_count:
                names_count[player_name] = 0
            else:
                names_count[player_name] += 1
                player_name = f"{player_name}{names_count[player_name] + 1}"
                 
            bot_boolean = str(input("IS THIS PLAYER A HUMAN? (Y/n)\t"))
            
            if bot_boolean == '':
                computer_player_dict[player_name] = False
            elif bot_boolean[0].lower() == 'y':
                computer_player_dict[player_name] = False  
            else:
                computer_player_dict[player_name] = True

        player_list = []
        for name, value in computer_player_dict.items():
            player = Player(name=name, computer=value)
            player_list.append(player)            

        game = Game(player_list)

        return game

game = setup_game()
 