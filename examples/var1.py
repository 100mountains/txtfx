#!/usr/bin/env python3

import sys
sys.path.append('../')
import manager as txt
import time
import random

if __name__ == '__main__':
	

	
	txt.eko('@typefx6 @FPS[15] @rndcase @red what the @green fuck, \n @magenta @rndcase MANY a day did i @yellow dream about @rndcase Laura... @blue @rndcase this is a great \n @rndcase big long @white test @grey string to see @cyan whats going on \n here...')

	
	exit()
	
	
	##########################++++++++++ END OF TEST SECTION ++++++++++#####################



	t2=txtfx('@typefx6 @[8]')
	t2.start()
	t2.stop()
	time.sleep(1)


	t2=txtfx('@[b1] bullet point 1')
	t2.start()
	time.sleep(3)
	t2.stop()


	t2=txtfx('@@')
	t2.start()
	time.sleep(1)
	t2.stop()

	t2=txtfx('@typefx5 @[1] @1;1 trying to print typefx next to each other... ')
	t2.start()
	time.sleep(1)
	t3=txtfx('@typefx1 @1;50 trying a dream...')
	t3.start()
	time.sleep(1)
	t4=txtfx('@typefx6 @1;69 work worky...')
	t4.start()
	time.sleep(3)
	t2.stop()
	t4.stop()
	t3.stop()
	time.sleep(2)
	print

	# demo
	t2=txtfx('@3;4 @typefx6 @[1] MANY a day did i dream about Laura...')
	t2.start()
	time.sleep(5)
	t2.stop()

	t2=txtfx('@typefx5 @[1] typefx5 MANY a day did i dream about Laura...')
	t2.start()
	time.sleep(5)
	t2.stop()
	print

	t2=txtfx('@typefx4 @[1] typefx4 MANY a day did i dream about Laura...')
	t2.start()
	time.sleep(5)
	t2.stop()

	t2=txtfx('@typefx3 @[1] typefx3 MANY a day did i dream about Laura...')
	t2.start()
	time.sleep(5)
	t2.stop()

	t2=txtfx('@typefx2 @[1] typefx2 normal left to right type effect LauLau...')
	t2.start()
	time.sleep(5)
	t2.stop()

	t2=txtfx('@typefx1 @[1] typefx1 word by word a day did i dream about Laura...')
	t2.start()
	time.sleep(5)
	t2.stop()
	print

	t2=txtfx('@txtcycle @spincycle @[8] @green this text has a colour cycling effect @txtcycle which can be @green turned off halfway through the string')
	t2.start()
	time.sleep(5)
	t2.stop()
	print

	t2=txtfx('@spincycle @[1] @green this @blue text @blue has @cyan a @yellow colour cycling @green spinner effect, the default typing effect, uses threads and a class ^grey and is programmed by me')
	t2.start()
	time.sleep(5)
	t2.stop()
	print

	t2=txtfx('@txtcycle @spincycle @[1] @green this text has a colour cycling @green effect as well @txtcycle which can be @green turned off halfway through the string')
	t2.start()
	time.sleep(5)
	t2.stop()
	print

	# clears screen
	t1=txtfx('@@').start()

	for x in range(1,9):
				t1=txtfx('@[%d] @grey spinner @red effect @blue number @yellow %d'%(x,x))
				t1.start()
				time.sleep(2)
				t1.stop()
	
	time.sleep(3)

	# clears screen
	t1=txtfx('@@').start()
	
	for x in range(1,4):
		t1=txtfx('@[b%d] @typefx0 @grey this @red is bullet point @blue %d @yellow @rndcase "this bit has random case" @rndcase and has typing effect "typefx0"'%(x,x))
		t1.start()
		time.sleep(0.5)
		t1.stop()
	
	t1=txtfx('@typefx1 @5;7 @[b1] @grey this @red text @blue has @cyan no @yellow spinner @green effect, and uses "typefx1" (word by word)')
	t1.start()
	time.sleep(3)
	t1.stop()

	t1=txtfx('@4;7 @[b2] [testing] @grey this @red text @blue has @yellow no @green spinner effect, and the default typing effect ("typefx2")')
	t1.start()
	time.sleep(4)
	t1.stop()
	print

	t4=txtfx('@22;22 @[3] this default coloured text appears at 22,22 and has spinner effect number ([3])')
	t4.start()
	time.sleep(5)
	t4.stop()
	print

	t2=txtfx('@spincycle @[1] @green this @blue text @blue has @cyan a @yellow colour cycling @green spinner effect, the default typing effect, uses threads and a class ^grey and is programmed by me')
	t2.start()
	time.sleep(5)
	t2.stop()
	print
	
