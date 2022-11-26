import enum
import random


class GameType(enum.IntEnum):
    CLASSIC = 0
    NEW = 1
    BIG = 2


FILE_LIST = [
    "./cubesets/16_classic.txt",
    "./cubesets/16_new.txt",
    "./cubesets/25.txt"
]

BOARD_SIZES = [4, 4, 5]

GAME_NAMES = [
    "Classic (4x4)",
    "Modern (4x4)",
    "Big Boggle (5x5)"
]


class BoggleBoard:
    board_string: list = None
    size: int = 0


class Cube:
    letter_list: list = None


def create_board(board_string: list, size: int) -> BoggleBoard:
    assert len(board_string) == size * size, \
        f"Length of board string must match its size squared ({len(board_string)} != {size * size})"
    board = BoggleBoard()
    board.board_string = board_string
    board.size = size
    return board


def create_cube(letter_list: list) -> Cube:
    assert len(letter_list) == 6, "Length of letter list must be 6"
    cube = Cube()
    cube.letter_list = letter_list
    return cube


def choose_random_letter(cube: Cube) -> str:
    ind = random.randrange(0, len(cube.letter_list))
    return cube.letter_list[ind]


def cubes_from_file(filename: str) -> list:
    with open(filename) as f:
        lines = f.read().splitlines()

    return [create_cube(line.title().split(" ")) for line in lines]


def board_from_cubelist(cubelist: list, gametype: GameType) -> BoggleBoard:
    boardsize = BOARD_SIZES[gametype]
    cubes = random.sample(cubelist, k=len(cubelist))
    cubes = cubes[0:boardsize ** 2]
    letters = [choose_random_letter(cube) for cube in cubes]
    return create_board(letters, boardsize)


def make_game(gametype: GameType = GameType.NEW) -> BoggleBoard:
    cubes = cubes_from_file(FILE_LIST[gametype])
    board = board_from_cubelist(cubes, gametype)
    return board
