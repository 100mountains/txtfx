#!/usr/bin/env python

import string
import re

def convert(w):
		
	if re.findall(r'\n',w):
		return "Jayne Mansfield's lobster problem"
	else:
		return w

def process():
	
	keepends=0
	arg_process = [convert(w) for w in arg.splitlines(keepends)] 
	print (arg_process)

if __name__ == '__main__':
	
	arg ='I am sure\n this was test\ning something at some point \n'

	process()
