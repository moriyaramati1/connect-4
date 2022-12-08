import alphaBetaPruning
import game
import screen
while True:

    this_game = game.create()
    screen.open_screen(this_game)

    while not game.is_finished(this_game):
        if game.is_human_turn(this_game):

            screen.playing(this_game)
            game.print_state(this_game)
        else:
            this_game = alphaBetaPruning.go(this_game)

    screen.finish_game(this_game)
    game.print_state(this_game)
