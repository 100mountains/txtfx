#!/usr/bin/env python3

import sys
sys.path.append('../')
import manager as txt
import time
import random

if __name__ == '__main__':
	

	
	txt.eko('@typefx6 @FPS[15] @rndcase @red what the @green heeelll, \n @magenta @rndcase MANY a day did i @yellow dream about @rndcase Laura... @blue @rndcase this is a great \n @rndcase big long @white test @grey string to see @cyan whats going on \n here...')


	txt.eko('@typefx6 @[8]')


	txt.eko('@[b1] bullet point 1')
	
	txt.eko('@@')
	

	txt.eko('@typefx5 @[1] @1;1 trying to print typefx next to each other... ')
	
	
	txt.eko('@typefx1 @1;50 trying a dream...')
	
	
	txt.eko('@typefx6 @1;69 work worky...')
	

	# demo
	txt.eko('@3;4 @typefx6 @[1] MANY a day did i dream about Laura...')

	txt.eko('@typefx5 @[1] typefx5 MANY a day did i dream about Laura...')
	
	time.sleep(5)
	
	txt.eko('@typefx4 @[1] typefx4 MANY a day did i dream about Laura...')
	
	time.sleep(5)

	txt.eko('@typefx3 @[1] typefx3 MANY a day did i dream about Laura...')
	
	time.sleep(5)

	txt.eko('@typefx2 @[1] typefx2 normal left to right type effect LauLau...')
	
	time.sleep(5)

	txt.eko('@typefx1 @[1] typefx1 word by word a day did i dream about Laura...')
	
	time.sleep(5)

	txt.eko('@txtcycle @spincycle @[8] @green this text has a colour cycling effect @txtcycle which can be @green turned off halfway through the string')
	
	time.sleep(5)
	
	txt.eko('@spincycle @[1] @green this @blue text @blue has @cyan a @yellow colour cycling @green spinner effect, the default typing effect, uses threads and a class ^grey and is programmed by me')
	
	time.sleep(5)

	txt.eko('@txtcycle @spincycle @[1] @green this text has a colour cycling @green effect as well @txtcycle which can be @green turned off halfway through the string')
	
	time.sleep(5)

	# clears screen
	txt.eko('@@').start()

	for x in range(1,9):
				txt.eko('@[%d] @grey spinner @red effect @blue number @yellow %d'%(x,x))		
				time.sleep(2)			

	# clears screen
	txt.eko('@@').start()
	
	for x in range(1,4):
		txt.eko('@[b%d] @typefx0 @grey this @red is bullet point @blue %d @yellow @rndcase "this bit has random case" @rndcase and has typing effect "typefx0"'%(x,x))
	
	
	txt.eko('@typefx1 @5;7 @[b1] @grey this @red text @blue has @cyan no @yellow spinner @green effect, and uses "typefx1" (word by word)')


	txt.eko('@4;7 @[b2] [testing] @grey this @red text @blue has @yellow no @green spinner effect, and the default typing effect ("typefx2")')
	

	txt.eko('@22;22 @[3] this default coloured text appears at 22,22 and has spinner effect number ([3])')
	

	txt.eko('@spincycle @[1] @green this @blue text @blue has @cyan a @yellow colour cycling @green spinner effect, the default typing effect, uses threads and a class ^grey and is programmed by me')
	
	time.sleep(5)
	
	
	exit()