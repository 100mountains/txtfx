#!/usr/bin/env python3

import sys
sys.path.append('../')
import manager as txt
import time
import random

if __name__ == '__main__':
	
	txt.eko ('@@')
	time.sleep(2)
	for blah in range(1,12):
		i = random.randint(1,30)
		x = random.randint(1,120)
		typernd = random.randint(1,6)
		colrnd = random.randint(0,255)
		txt.eko ('@typefx%d @%d;%d'%(typernd,i,x) + ' @FPS[13] @C[%d]' %(colrnd) + ' Full test of string\n \
		much shorter string \n \
		again, a little bit longer....')
		time.sleep(0.1)
		
	time.sleep(5)
	txt.eko ('@@')
	
	#txt.eko ('@typefx2 @2;8 @C[77] Full test @bold of @underline string @underline \n \
	#		@reverse much shorter @bold string \n \
	#		@bold again, a little bit @underline longer....')
	#exit()
	
	#for whateverrrr in range(1,6):
	#	
#	
#		for blah in range(1,12):
#			i = random.randint(1,30)
#			x = random.randint(1,120)
#			typernd = random.randint(1,6)
#			colrnd = random.randint(0,255)
#			txt.eko ('@typefx2 @%d;%d'%(i,x) + ' @C[%d]' %(colrnd) + ' @rainbow Full test @bold of @underline string @underline \n \
#			@reverse much shorter @bold string \n \
#			again, a little @rainbow bit @underline longer....')
#			time.sleep(1.2)
#			txt.eko ('@@')
#		time.sleep(1.5)
#

#	exit()
		
	txt.eko ('@@ @typefx3 @rainbow @12;12 In la la la la la an open, unmulched area, @bold the tool of choice is a scuffle or stirrup hoe, which you push and pull across the ground to sever\n \
		much shorter string \n \
		again, a little bit longer string than that....')
		
	txt.eko ('@typefx0 @rainbow this stuff will appear immediately, the tool of choice is a scuffle or stirrup hoe, which you push and pull across the ground to sever\n \
		much shorter string \n \
		again, a little bit longer string than that....')
	
	txt.eko('@typefx6 @FPS[15] @rndcase @red what the @green, \n @magenta @rndcase MANY a day did i @yellow dream about @rndcase Laura... @blue @rndcase this is a great \n @rndcase big long @white test @grey string to see @cyan whats going on \n here...')

	
	exit()
	
	
	##########################++++++++++ END OF TEST SECTION ++++++++++#####################