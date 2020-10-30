#!/usr/bin/python3

"""Starts a command line game."""

from tic_tac_toe import game

import sys # for PI experiment

def main():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        print('Running in a PyInstaller bundle.')
    else:
        print('Running in a normal Python process.')
    game.Game().main()

if __name__ == '__main__':
    main()
