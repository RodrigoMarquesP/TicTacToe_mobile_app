# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 12:59:22 2020.

@author: sucod

Icon made by monkik from "https://www.flaticon.com/"
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from random import choice

from numpy import array, zeros, count_nonzero, ndenumerate, copy, where
from numpy import sum as sm
from numpy.random import shuffle


#################### MINIMAX LOGICS #########################################


def minimax_move(actual_state: array) -> array:
    """
    Find the optimal move in a tictactoe game with recursive depth search.

    Parameters
    ----------
    actual_state : numpy.array
        3x3 array that describes the actual state of the game.

    Returns
    -------
    numpy.array
        3x3 array that describes the best move to be done.

    """
    move_utility = []
    moves = valid_moves(actual_state)
    for move in moves:
        v = minvalue(move)
        if v == 1:  # in case of 1 utility - win -, select this move
            return move
        else:
            # in case of non garanted winning, we look for all states
            # and list its utilitys
            move_utility.append(v)
    try:
        # try to find an "tied utility move", since wasn't a certain win
        return moves[move_utility.index(0)]
    except ValueError:
        # return any move, since all of them lead to a defeat
        # NOTE: this try/except is just for debuging and testing
        # purpose, since the algorithm will never lose in a normal
        # game, so, the ValueError will never happen
        return moves[0]


def valid_moves(state: array, marker: int = 1) -> array:
    """
    Generate the valid moves for a given state of the game.

    Parameters
    ----------
    state : numpy.array
        3x3 array that describes the state node of the game.
    marker : int, optional
        Mark the valid moves (1 for machine, -1 for oponent). The default is 1.

    Returns
    -------
    moves : numpy.array
        A array of all the possible moves in the node.

    """
    n_moves = 9 - count_nonzero(state)  # counting the valid moves
    moves = zeros((n_moves, 3, 3), dtype='int8')  # a array of states
    for index, item in ndenumerate(state):
        if item == 0:  # if isn't a mark in this position
            new = copy(state)
            new[index] = marker  # mark
            moves[n_moves - 1] = new  # put the new move in the moves array
            n_moves -= 1  # ajust the position of the next new state
    shuffle(moves)  # shuffle the moves
    # the reason of shuffling the states array is to make the
    # moves less predictable, making the machine select any of
    # the states with higher utility
    return moves


def minvalue(state: array) -> int:
    """
    Simulate the perfect oponent move - lower utility.

    Parameters
    ----------
    state : numpy.array
        Actual node of the search.

    Returns
    -------
    v : int
        Utility of node according to minimax logics.

    """
    for v in terminal_test(state):
        # using a 'for block' with a single element list
        # allow us to return the utility of the state
        # if it's a terminal one, without a couple of 'if blocks'
        return v
    v = 2  # higher than any real utility
    for move in valid_moves(state, marker=-1):
        # Select the lower utility move between the machine moves
        v = mini(v, maxvalue(move))
    return v


def maxvalue(state: array) -> int:
    """
    Choose the best move for the machine - higher utility.

    Parameters
    ----------
    state : numpy.array
        Actual node of the search.

    Returns
    -------
    v : int
        Utility of node according to minimax logics.

    """
    for v in terminal_test(state):
        # using a 'for block' with a single element list
        # allow us to return the utility of the state
        # if it's a terminal one, without a couple of 'if blocks'
        return v
    v = -2  # lower than any real utility
    for move in valid_moves(state):
        # Select the higher utility move between the oponent moves
        v = maxi(v, minvalue(move))
    return v


def mini(a: int, b: int) -> int:
    """
    Return the lower of two arguments.

    Parameters
    ----------
    a : int
        A utility value.
    b : int
        A utility value.

    Returns
    -------
    int
        The lower between the two parameters.

    """
    return a if b > a else b


def maxi(a: int, b: int) -> int:
    """
    Return the higher of two arguments.

    Parameters
    ----------
    a : int
        A utility value.
    b : int
        A utility value.

    Returns
    -------
    int
        The higher between the two parameters.

    """
    return a if a > b else b


def terminal_test(node: array) -> list:
    """
    Return the utility of the state.

    ([] if its not a terminal node)
    ([1] if its a winning node)
    ([-1] if its a losing node)

    Parameters
    ----------
    node : np.array
        Actual node of the search.

    Returns
    -------
    list
        A single element list with the utility of the requested node.

    """
    if 3 in sm(node, axis=0) or 3 in sm(node, axis=1):
        return [1]
    if (node[(0, 0)] + node[(1, 1)] + node[(2, 2)]) == 3:
        return [1]
    if (node[(0, 2)] + node[(1, 1)] + node[(2, 0)]) == 3:
        return [1]
    if -3 in sm(node, axis=0) or -3 in sm(node, axis=1):
        return [-1]
    if (node[(0, 0)] + node[(1, 1)] + node[(2, 2)]) == -3:
        return [-1]
    if (node[(0, 2)] + node[(1, 1)] + node[(2, 0)]) == -3:
        return [-1]
    if count_nonzero(node) == 9:
        # non-terminal state
        return [0]
    return []


############################ APPLICATION LOGICS #############################

# setting the background color as black
Window.clearcolor = (0, 0, 0, 1)

# Setting the screen size
# Window.size = (360, 600)
# We use the line above for vizualizing how the screen will look in
# a mobile device, but it can't be used for the mobile application
# cause it limits the screen size.


class MainGrid(Widget):
    """Interface class."""

    # the static variables:
    # 9 variables, one for each button
    # 1 variable for the retry button
    # 1 variable for the result button (only for display purpose)
    zerozero = ObjectProperty(None)
    zeroone = ObjectProperty(None)
    zerotwo = ObjectProperty(None)
    onezero = ObjectProperty(None)
    oneone = ObjectProperty(None)
    onetwo = ObjectProperty(None)
    twozero = ObjectProperty(None)
    twoone = ObjectProperty(None)
    twotwo = ObjectProperty(None)
    retrybtn = ObjectProperty(None)
    result = ObjectProperty(None)
    allow_clear = False
    player_round = True
    player_starts_next = False
    first_move = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load("main_music.wav")
        self.sound.loop = True
        #self.sound.play()  ###############################################################################

    def btn(self, button):
        """
        Mark the button if thats allowed.

        Parameters
        ----------
        button : kivy.properies.ObjectProperty
            A button that represents a place on the game.

        Returns
        -------
        None.

        """
        if button.text == "" and self.player_round and self.result.text == "":
            button.text = "X"
            self.verify()
            self.player_round = False

    def call_minimax(self, dt):
        """Do all procedure of the machine round."""
        if self.first_move and not self.player_round:
            coords = where((self.give_state()) == -1)
            self.first_move_marker(coords)
            self.first_move = False
            self.player_round = True
        elif self.result.text == "" and not self.player_round:
            state = self.give_state()
            next_move = minimax_move(state)
            coord = where((next_move - state) == 1)
            self.mark(coord)
            self.verify()
            self.player_round = True

    def first_move_marker(self, coords):
        """Call mark function with a if-else statement."""
        if coords in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            self.mark((1, 1))
        elif coords == (1, 1):
            self.mark(choice([(0, 0), (0, 2), (2, 0), (2, 2)]))
        elif coords == (0, 1):
            self.mark(choice([(coords[0], choice([0, 2])),
                              (choice([1, 2]), coords[1])]))
        elif coords == (1, 2):
            self.mark(choice([(coords[0], choice([0, 1])),
                              (choice([0, 2]), coords[1])]))
        elif coords == (2, 1):
            self.mark(choice([(coords[0], choice([0, 2])),
                              (choice([0, 1]), coords[1])]))
        else:
            self.mark(choice([(coords[0], choice([1, 2])),
                              (choice([0, 2]), coords[1])]))

    def mark(self, coord):
        """Mark the move on the table."""
        if coord == (0, 0):
            self.zerozero.text = "O"
        elif coord == (0, 1):
            self.zeroone.text = "O"
        elif coord == (0, 2):
            self.zerotwo.text = "O"
        elif coord == (1, 0):
            self.onezero.text = "O"
        elif coord == (1, 1):
            self.oneone.text = "O"
        elif coord == (1, 2):
            self.onetwo.text = "O"
        elif coord == (2, 0):
            self.twozero.text = "O"
        elif coord == (2, 1):
            self.twoone.text = "O"
        else:
            self.twotwo.text = "O"

    def give_state(self):
        """
        Read the text from the buttons and gerrerates a corresponding array.

        Returns
        -------
        numpy.array
            A representation of the table.

        """
        state = []
        state.append([self.zerozero.text, self.zeroone.text, self.zerotwo.text])
        state.append([self.onezero.text, self.oneone.text, self.onetwo.text])
        state.append([self.twozero.text, self.twoone.text, self.twotwo.text])
        for i, e in enumerate(state[:]):
            for i2, e2 in enumerate(e):
                if e2 == "X":
                    state[i][i2] = -1
                elif e2 == "O":
                    state[i][i2] = 1
                else:
                    state[i][i2] = 0
        return array(state)

    def verify(self):
        """
        Call 'teste_terminal' in the actual state to set the game result.

        Returns
        -------
        numpy.array
            A representation of the table.

        """
        state = self.give_state()
        res = terminal_test(state)
        for r in res:
            if r == 0:
                self.result.text = "TIED GAME"
                self.allow_clear = True
            elif r == 1:
                self.result.text = "YOU LOSE"
                self.allow_clear = True
            elif r == -1:
                self.result.text = "YOU WIN"
                self.allow_clear = True
        return state

    def clear(self):
        """Clear the table and manage the first player."""
        if self.allow_clear:
            self.zerozero.text = ""
            self.zeroone.text = ""
            self.zerotwo.text = ""
            self.onezero.text = ""
            self.oneone.text = ""
            self.onetwo.text = ""
            self.twozero.text = ""
            self.twoone.text = ""
            self.twotwo.text = ""
            self.result.text = ""
            self.allow_clear = False
            if not self.player_starts_next:
                self.mark((choice([0, 1, 2]), choice([0, 1, 2])))
                self.player_round = True
                self.player_starts_next = True
            else:
                self.player_starts_next = False
                self.first_move = True
                self.player_round = True


class MyApp(App):
    """Application class, heriting from App class."""

    def build(self):
        """Build the application."""
        self.icon = 'grandmother.png'
        game = MainGrid()
        Clock.schedule_interval(game.call_minimax, 1.0/2)
        return game


if __name__ == "__main__":
    MyApp().run()
