import math
import sys
import pygame
import game
from game import Game

pygame.init()

BOARD_SIZE = 7
SQUARE_SIZE = 100
COLUMN_COUNT = game.Game().columns
ROW_COUNT = game.Game().rows
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARE_SIZE / 2 - 5)

WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (255, 255, 0)
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
BLUE_COLOR = (0, 0, 255)

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Connect 4!')

main_font = pygame.font.SysFont("cambria", 25)


class Button:

    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, BLUE_COLOR)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        """
        This function draws images to the screen
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_click(self, position):
        """
        :param position: Gets the coordinate of the pressed position
        :return: True if its in the button area ( the button clicked)
        """
        x_pos = position[0]
        y_pos = position[1]
        if x_pos in range(self.rect.left, self.rect.right) and y_pos in range(self.rect.top, self.rect.bottom):
            return True

    def change_color(self, position):
        """
        This function change the color of the button's text
        :param position: Gets the coordinate of the pressed position
        """
        x_pos = position[0]
        y_pos = position[1]
        if x_pos in range(self.rect.left, self.rect.right) and y_pos in range(self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, RED_COLOR)
        else:
            self.text = main_font.render(self.text_input, True, WHITE_COLOR)


def open_screen(game_state: Game):
    """
    This function responsible of the open screen, create two buttons of the starting player,
    and waits for the human decision
    :param game_state: The game object
    """
    screen.fill(WHITE_COLOR)
    font = pygame.font.SysFont("comicsansms", 50)
    label = font.render("Welcome To Connect-4!", True, BLUE_COLOR)
    screen.blit(label, (SQUARE_SIZE, int(HEIGHT // 2) - 2 * SQUARE_SIZE))
    label = font.render("Who Plays First?", True, BLUE_COLOR)
    screen.blit(label, (SQUARE_SIZE * 1.5, int(HEIGHT // 2) - SQUARE_SIZE))
    button_surface = pygame.image.load("button.jpg")
    button_surface = pygame.transform.scale(button_surface, (150, 100))
    button1 = Button(button_surface, SQUARE_SIZE * 2.5, int(HEIGHT // 2) + 0.5 * SQUARE_SIZE, "Computer")

    button2 = Button(button_surface, SQUARE_SIZE * 5, int(HEIGHT // 2) + 0.5 * SQUARE_SIZE, "Human")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.check_for_click(pygame.mouse.get_pos()):
                    game_state.player = game.Player.Computer
                    return game_state

                if button2.check_for_click(pygame.mouse.get_pos()):
                    game_state.player = game.Player.Human
                    return game_state

        button1.update()
        button2.update()

        button1.change_color(pygame.mouse.get_pos())
        button2.change_color(pygame.mouse.get_pos())
        pygame.display.update()


def draw_board(game_state: Game):
    """
    This function draws the game board
    :param game_state: The game object
    """
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE_COLOR,
                             (col * SQUARE_SIZE, row * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if game_state.game_board[row][col] == game.Player.Human:
                pygame.draw.circle(screen, YELLOW_COLOR, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            elif game_state.game_board[row][col] == game.Player.Computer:
                pygame.draw.circle(screen, RED_COLOR, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
            else:
                pygame.draw.circle(screen, BLACK_COLOR, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   RADIUS)
    pygame.display.update()


def available_col(game_state: Game, column):
    """
    This function checks if the column is not filled.
    :param game_state:  The game object
    :param column: the column the user want to put his marker
    :return: true if this column is not filled
    """
    return not game_state.filled_column(column)


def finish_game(game_state: Game):
    """
    This function write what the game result.
    :param game_state:  The game object
    """
    pygame.draw.rect(screen, BLACK_COLOR, (0, 0, WIDTH, SQUARE_SIZE))
    font = pygame.font.SysFont("monospace", 45)
    draw_board(game_state)

    if game.value(game_state) == game.Status.VICTORY:
        label = font.render("I Win, You Such A Loser!", True, RED_COLOR)
    elif game.value(game_state) == game.Status.LOSS:
        label = font.render("You Did It!", True, RED_COLOR)
    else:
        label = font.render("It's A Tie!", True, RED_COLOR)

    screen.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(3000)
    sys.exit()


def playing(game_state: Game):
    """
    This function control the game screen
    :param game_state: The game object
    :return: The game object for the computers turns.
    """
    draw_board(game_state)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK_COLOR, (0, 0, WIDTH, SQUARE_SIZE))
                mouse_x = event.pos[0]  # x coordinate
                if game_state.player == game.Player.Human:
                    pygame.draw.circle(screen, YELLOW_COLOR, (mouse_x, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, RED_COLOR, (mouse_x, int(SQUARE_SIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x = event.pos[0]  # x coordinate
                clicked_col = int(math.floor(mouse_x // SQUARE_SIZE))
                print(game_state.game_board)
                print(available_col(game_state, clicked_col))
                if available_col(game_state, clicked_col) and 0 <= clicked_col <= COLUMN_COUNT:
                    row = game_state.find_row(clicked_col)
                    game.make_move(game_state, row, clicked_col)
                    draw_board(game_state)

                    return game_state

        pygame.display.update()
