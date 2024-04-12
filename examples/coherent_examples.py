#!/usr/bin/env python3

import sys
sys.path.append('../')
import manager as txt
import time

def demonstrate_typefx1():
    effect = txt.txtFX('@typefx1 @rainbow @12;12 "In an open, unmulched area, the tool of choice is a scuffle hoe."')
    effect.start()
    time.sleep(5)
    effect.stop()

def demonstrate_typefx2():
    effect = txt.eko('@typefx2 @bold "Much shorter string with bold effect."')
    effect.start()
    time.sleep(5)
    effect.stop()

def demonstrate_spin_cycle():
    effect = txt.eko('@spincycle @[1] @green "This text has a spinning effect with green color."')
    effect.start()
    time.sleep(5)
    effect.stop()

def demonstrate_txt_cycle():
    effect = txt.eko('@txtcycle @spincycle @[8] @green "This text has a colour cycling effect."')
    effect.start()
    time.sleep(5)
    effect.stop()

if __name__ == '__main__':
    demonstrate_typefx1()
    demonstrate_typefx2()
    demonstrate_spin_cycle()
    demonstrate_txt_cycle()
