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


def jogada_minimax(estado_atual):
    """Receive the actual state snd returns the better move."""
    estado_atual = array(estado_atual)
    for v in teste_terminal(estado_atual):
        return v
    utilidade = []
    jogadas = jogadas_validas(estado_atual)
    for jogada in jogadas:
        v = valormin(jogada)
        if v == 1:
            return jogada
        else:
            utilidade.append(v)
    try:
        return jogadas[utilidade.index(0)]
    except ValueError:
        return jogadas[0]


def jogadas_validas(estado, marcar=1):
    """Return all possible mmoves in the actual state."""
    n_jogadas = 9 - count_nonzero(estado)
    jogadas = zeros((n_jogadas, 3, 3), dtype='int8')
    for index, elemento in ndenumerate(estado):
        if elemento == 0:
            novo = copy(estado)
            novo[index] = marcar
            jogadas[n_jogadas - 1] = novo
            n_jogadas -= 1
    shuffle(jogadas)
    return jogadas


def valormin(estado):
    """Look for the minimun utility value at the knot."""
    for v in teste_terminal(estado):
        return v
    v = 2
    for jogada in jogadas_validas(estado, marcar=-1):
        v = mini(v, valormax(jogada))
    return v


def valormax(estado):
    """Look for the maximun utility value at the knot."""
    for v in teste_terminal(estado):
        return v
    v = -2
    for jogada in jogadas_validas(estado):
        v = maxi(v, valormin(jogada))
    return v


def mini(a, b):
    """Return the minumun between two values."""
    return a if b > a else b


def maxi(a, b):
    """Return the maximun between two values."""
    return a if a > b else b


def teste_terminal(no):
    """Returns the utility of a terminal knot or nothing in a non terminal."""
    if 3 in sm(no, axis=0) or 3 in sm(no, axis=1):
        return [1]
    if (no[(0, 0)] + no[(1, 1)] + no[(2, 2)]) == 3:
        return [1]
    if (no[(0, 2)] + no[(1, 1)] + no[(2, 0)]) == 3:
        return [1]
    if -3 in sm(no, axis=0) or -3 in sm(no, axis=1):
        return [-1]
    if (no[(0, 0)] + no[(1, 1)] + no[(2, 2)]) == -3:
        return [-1]
    if (no[(0, 2)] + no[(1, 1)] + no[(2, 0)]) == -3:
        return [-1]
    if count_nonzero(no) == 9:
        return [0]
    return []


############################ APPLICATION LOGICS #############################

Window.clearcolor = (0, 0, 0, 1)
# Window.size = (360, 600)


class MainGrid(Widget):
    """Interface class."""

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
        self.sound.play()

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
            next_move = jogada_minimax(state)
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
        res = teste_terminal(state)
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
