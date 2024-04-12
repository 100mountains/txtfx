#!/usr/bin/env python3
# "The Jayne Mansfield Lobster Problem"
# deals with the rainbow and continuation over newlines...
# and thread management, stopping etc....

from sys import stdout
import txtFX as t  # does all the work
import time  # relative import
import re  # regeX bollox
import subprocess  # for debugging
import os
import threading  # terminal variables

term_types = ['Eterm-256color', 'gnome-256color', 'konsole-256color', 'putty-256color', 'rxvt-256color',
              'screen-256color', 'screen-256color-bce', 'screen-256color-bce-s', 'screen-256color-s',
              'xterm-256color', 'xterm+256color']
terminaltype = None
DEBUG = 'ffON'

if DEBUG == 'ON':
    fd = open("output", "w")
    subprocess.Popen(["xterm", "-geometry", "100x40-0+0", "-T", "DEBUG OUTPUT", "-e", "tail", "-f", "output"])

def debug(txt=None):
    if DEBUG == 'ON':
        fd.write(txt)
        fd.flush()

def termtype():
    terminaltype = os.environ["TERM"]
    if terminaltype not in term_types:
        print("Sorry, your terminal doesn't support colour. Sort your fscking life out, this is the 21st century bud.")
        print("You currently have your TERM variable set to: " + terminaltype)
        print("Try 'TERM=' and one of these...")
        for termlist in term_types:
            print(termlist)
        print()
        exit()

def eko(eko):
    termtype()  # check if term is good....
    t1 = t.txtfx(eko)
    t1.start()

if __name__ == '__main__':
    # check terminal type
    termtype()