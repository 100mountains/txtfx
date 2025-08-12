# main.py
import os
from input_parser import InputParser
from animation_engine import AnimationEngine
from constants import term_types

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
    config = InputParser.parse_input(eko)
    t1 = AnimationEngine(config)
    t1.start()

if __name__ == '__main__':
    termtype()

    # Example usage
    eko("@blue This is a ^red^test @blink of the emergency ^white^broadcast system.")