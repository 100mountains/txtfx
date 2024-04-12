#!/usr/bin/env python3
# vim:fileencoding=utf8

import rgb2ansi as colourspace
from sys import stdout
import random
import math
import string
import sys
import time
import threading
import re # for returns 
import subprocess # for debugging

__author__ = 'n01'
__author_email__ = 'n01@mailinator.com'
__date__ = '03-03-2012'
__version__ = '0.4'

DEBUG='OffN'

if DEBUG == 'ON':
    fd = open("output", "w")
    subprocess.Popen(["xterm", "-geometry", "100x40-0+0", "-T", "DEBUG OUTPUT", "-e", "tail", "-f", "output"])

esc = '\033['
#reset = '%s0m'%esc
reset = ''
format = '\033[0;%dm'
attrformat = '\033[%dm'
testesformat = '%d;0m'
format256 = '38;5;%dm'
fgoffset, bgoffset = 30, 40

#attrs = dict ((name, val) for val, name in enumerate('none bold faint italic underline blink fast reverse concealed' .split()))
attrs =   {'none': 0, 'bold': 1, 'faint': 2, 'fast': 6, 'blink': 5, 'concealed': 8, 'italic': 3, 'underline': 4, 'reverse': 7}

colours = dict((name, val) for val, name in enumerate('grey red green yellow blue magenta cyan white' .split()))
keywords = ['typefx0', 'typefx1', 'typefx2', 'typefx3', 'typefx4', 'typefx5', 'typefx6', 'spincycle', 'txtcycle', 'rainbow', 'rndcase', 'cursoron', 'cursoroff']

# put bold escapes in
bpoints = ( "[*]", "[!]", "[@]" )

spinners= ( "|/-\\" , ".o0O0o. " , "⇐⇖⇑⇗⇒⇘⇓⇙" , "◓◑◒◐" , "○◔◑◕●" , "◴◷◶◵" , "▏▎▍▌▋▊▉█▉▊▌▍▎" , "▁▂▃▄▅▆▇█▇▆▅▄▃▂" )

colist='grey blue cyan white cyan blue'.split()
colist1='blue cyan'.split()

class txtfx(threading.Thread): 

    def __init__(self,arg=None):
        super(txtfx,self).__init__()
        
        # thread attributes
        self._stop = False
        self.name="_txtfx_"
        
        self.debug ("current thread :%s"%threading.currentThread() )
        self.debug ( "thread count :%s"%threading.activeCount() )    
        
        # defaults
        self.arg = arg
        self.lines = []
        self.startline = 0

        
        # terminal crap
        self.cursave='\033[s'
        self.curload='\033[u'
        self.curup='\033[%dA'
        self.cursor_override = None # cursor over ride setting
        
        # timing
        self.FPS = 30
        self.FPS_override = None
        self.last_time = None
        self.new_time = None

        # colour defaults
        #self.spincolour = '\x1b[0m\x1b[1;32m' 
        self.spincolour = '\x1b[1;32m' 
        #self.highlight_colour = '\x1b[0m\x1b[38;5;255m' 
        self.highlight_colour = '\x1b[38;5;255m' 
        #self.last_colour ='\033[0m'
        self.last_colour =''
        self.colour = self.last_colour
        self.colourspace = [] # colour for each character in a list
        self.rev_colourspace = [] # duh
        
        # attributes
        self.attrcodes = ''    
        self.currentattrs = list()
        self.attrspace = []
        
        stdout.write('\033[0m') # for attributes
        
        # rainbow sheet
        self.rainbow = 0        # 0 is off (default), 1 is on - taste teh rainbow
        self.rainanim = 0        # iterate through rainbow
        
        # animation variables
        self.txtpos=1
        self.initpos=1
        self.spinpos=1
        self.colpos=0     # used for colour cycling the spinner
        self.txtcolpos=0  # used for colour cycling the text
        self.spinanim=0   # ?
        self.rndcase=0     # 0 is off, 1 is on
        self.spsw=0          # 0 is off, 1 -7 are different types
        self.typefx=2        # 0 is off, 1 is word, 2 is letter  (default)
        self.spincycle=0      # 0 is off (default), 1 is on
        self.txtcycle=0       # 0 is off (default), 1 is on

        self.txtfxpos=0         # for matrix effect
        self.txt= []              # for matrix effect
        self.shuffle_array= []  # for shuffle matrix effect
    
    def timer (self,go=None):
        
        if go == 'go':
            self.last_time = time.time()
        else:
            self.new_time = time.time()
            sleepy_time = ((1000.0 / (self.FPS*2)) - (self.new_time - self.last_time)) / 1000.0
            
            if sleepy_time > 0:
                time.sleep(sleepy_time)
                
            self.last_time = self.new_time
            
    def debug (self,txt=None):
        if DEBUG == 'ON':
            fd.write(str(txt) + '\n')
            fd.flush()

    def thread_debug(self):
            
        self.debug ("threading enumerate :%s"%threading.enumerate() )
        self.debug ("current thread :%s"%threading.currentThread() )
        self.debug ( "thread count :%s"%threading.activeCount() )    
                

    def set_cursor(self):
            
        #over ride cursor setting

        if self.cursor_override == 1:
            self.cursor_visible()
        elif self.cursor_override == 0:
            self.cursor_invisible()
    


    def cursor_visible(self):
        stdout.write("\033[?25h")    
    def cursor_invisible(self):
        stdout.write("\033[?25l")    
    def stop(self):
        self._stop = True 
        self.cursor_visible()
        stdout.write("\033[0m") # restore default text
    def stopped(self):
        return self._stop == True
    def __exit__(self, type, value, traceback):
        return isinstance(value, TypeError)

    def spin_advance (self,x):

        if self.spsw != 0:
            # colour cycling
            if self.spincycle:
                blah = [reset]
                tmpword = colist[self.colpos]
                blah.append(format % (colours[tmpword]+fgoffset))
                self.spincolour = esc.join(blah)
                
            # only animate spinner every x rounds
            if self.clock_res == 1:
            
                stdout.write(self.spincolour + '\033[%dG'%self.spinpos + "{"+self.chars[self.spinanim].decode("utf-8") + "}"),
                stdout.flush()
                self.spinanim+=1
                self.spinanim%=len(self.chars)
                self.colpos+=1
                self.colpos%=len(colist)
            
            if self.clock_res >= x:
                self.clock_res=0
            else:
                self.clock_res+=1

    def esc_convert(self,w):
        
        word = w
        # is we a command?
        truth = word.startswith(('^','@'))

        cmd = [reset] 
        # CHANGE THIS to attrs list to start, dont need to reset if attirbutes or do we, reset then attrs ? try just attrs first...

        if truth:
            # examine 2nd character onwards from word ie get rid of '@'
            tmpword = word[1:]
            
            # check for a colour word command
            if tmpword in colours:
                # foreground colour
                if word.startswith('@'):
                    tmpoffset=fgoffset
                # background colour
                elif word.startswith('^'):
                    tmpoffset=bgoffset
                cmd.append(format % (colours[tmpword]+tmpoffset))
                self.colour = esc.join(cmd)
                return truth, None, self.colour
            
            # ---- ATTRIBUTES ----
            # if command in global list of attirbutes
            if tmpword in attrs:    
                
                # if property is already selected toggle it
                if tmpword in self.currentattrs:
                    self.currentattrs.remove(tmpword)
                    self.debug(str(self.currentattrs) + '\n\n' + str(attrs) + '\n\n')
                    
                        
                # if property is selected add it to the list
                else:
                    self.currentattrs.append(tmpword)
                
                for blerp in self.currentattrs:
                    c=attrformat % attrs[blerp]
                    cmd.append(c)
                    
                self.debug('\n\n\nHERE IS WHAT YER WANT\n')
                self.debug(str(self.currentattrs) + '\n\n' + str(attrs) + '\n\n')

                return truth, None, self.colour

            # check for keywords
            if tmpword in keywords:
                if tmpword == 'rndcase':
                    # toggle case on / off
                    self.rndcase = not self.rndcase
                    return truth, None, self.colour
                # number of type fx available
                if tmpword.startswith('typefx') and 0 <=int(tmpword[-1]) <=6: 
                    # set typing effect 0=off, 1=word, 2=letter
                    self.typefx=int(tmpword[-1])
                    return truth, None, self.colour
                if tmpword == 'spincycle': 
                    self.spincycle = not self.spincycle # toggle
                    return truth, None, self.colour
                if tmpword == 'txtcycle': 
                    self.txtcycle = not self.txtcycle
                    return truth, None, self.colour
                if tmpword == 'rainbow':
                    self.rainbow = not self.rainbow
                    return truth, None, self.colour
                if tmpword == 'cursoron':
                    self.cursor_override = 1
                    return truth, None, self.colour
                if tmpword == 'cursoroff':
                    self.cursor_override = 0
                    return truth, None, self.colour
                    
            # spinner and bullet point command
            if tmpword.startswith('[') and tmpword[-1] == ']':
                # check for one of three bullet points - could this be better with regex?
                # we dont want to catch too many malformed commands eg @[bblah] etc...
                if tmpword[1] == 'b':
                    if 1 <= int(tmpword[2]) <= len(bpoints):
                        return False, bpoints[int(tmpword[2])-1], self.colour
                    else:
                        return False, word, self.colour
                # check for spinners 
                if 1 <= int(tmpword[1]) <= len(spinners):
                    self.spsw = int(tmpword[1:-1])
                    #convert the utf8 spinner string to a list
                    self.chars=[c.encode("utf-8") for c in spinners[self.spsw-1]]
                    # do not enter anything into the tuple seeing as we arent going to print this 
                    return truth, None, self.colour
            
            # frame rate over-ride
            if tmpword.startswith('FPS') and tmpword[3] == '[' and tmpword[-1] == ']': 
                    self.FPS_override = int(tmpword[4:-1])
                    return truth, None, self.colour
                    
            # 256 colour number @C[1]
            if tmpword.startswith('C[') and tmpword[-1] == ']': 
                    tmpcolour = int(tmpword[2:-1])
                    cmd.append(format256 % tmpcolour)
                    self.colour = esc.join(cmd)
                    return truth, None, self.colour
            
            # positioning (starts with @)
            if tmpword=='@':
                # clear the screen
                cmd.append('2J')
                cmd.append('H')
                return truth, esc.join(cmd), self.colour
            # could be a more robust check - quick and dirty
            elif ';' in tmpword:
                # move cursor position
                cmd.append('%sH'%tmpword)
                # set initpos column to initial text x position
                self.initpos=int(tmpword.split(';')[1]) # puts x position in self.initpos
                self.startline=int(tmpword.split(';')[0]) # puts y position in self.startline
                return truth, esc.join(cmd), self.colour
            
        else:
            if self.rndcase:
                word = ''.join(random.choice((str.upper,str.lower))(x) for x in word)
                # below code is actually faster, but i find the above more compact 
                #caps = word[1].upper()
                #lowers = word[1].lower()
                #self.arg_process[listindex] = ''.join(random.choice(x) for x in zip(lowers, caps))
            
            #self.attrcodes = ''    
            self.attrcodes = '\x1b[0m'
            # create attribute codes for current word
            for blerp in self.currentattrs:
                c=attrformat % attrs[blerp]
                self.attrcodes += c
            #esc.join(attrcodes)
            #self.debug(str(attrcodes))
            #self.attrspace.append(attrcodes)
            # build colourspace - this is where to put txtcycle as well....
            for t in word:
                
                if self.rainbow == 1:
                #    # append rainbow self.colourspace.append(self.colour)
                    self.colourspace.append(self.rainbow_cycle())
                else:
                    self.colourspace.append(self.colour) # add basecolour to character colour map
                
                # build attrspace
                #self.debug(str(self.currentattrs))
                self.attrspace.append( self.attrcodes )

            # change this to be an if for (IF NOT LAST WORD - cos its adding one space to the end)
            # something like this:
            #        self.debug(str(self.arg_process[-1][1]))
            #            self.debug(str(word[1]))
            #        #if word=self.arg_process[-1]
            self.debug(str(self.attrspace))
            self.colourspace.append(self.colour) # add a space to the character map between words
            #self.attrspace.append( '\033[0m') # add a space to attribute map between words - could reset here
            self.attrspace.append( '') # add a space to attribute map between words - could reset here
            return truth, word, self.colour

    def process(self,line):
                    

        # split the line up into true and false statement values and text arg_process[0] = truth test, [1] = command or text
        # self.esc_convert should return a tuple - ie thats why theres a function here that returns two values...
        self.arg_process = [self.esc_convert(w) for w in line.split()] 
        
        # text only string for effects
        for i,word in enumerate(self.arg_process):
            if word[0] is False:
                self.txt.append(self.arg_process[i][1])
                
        self.txt=' '.join(self.txt)
        self.txtlen = len(self.txt)
        self.shuffle_array = self.shuffle(self.txt)    
        self.cap_array = self.invert_caps(self.txt)    
        self.word_array = list(self.txt.split())
        
        # reverse colourspace 
        self.rev_colourspace = self.colourspace[::-1]
        
        # DEBUG STUFF 
        self.debug('self.arg_process: ' + str(self.arg_process) + '\n\n')
        #self.debug('self.colourspace: ' + str(self.colourspace) + '\n\n')
        self.debug('self.shuffle_array: ' + str(self.shuffle_array) + '\n\n')
        #self.debug('self.cap_array: ' + str(self.cap_array) + '\n\n')
        #self.debug('self.txt: ' + str(self.txt) + '\n\n')
        #self.debug('self.txtlen: ' + str(self.txtlen) + '\n\n')
        #self.debug('self.colourspace length: ' + str(len(self.colourspace)) + '\n\n')
        #self.debug('self.word_array: ' + str(self.word_array) + '\n\n')
            
    def process_lines(self,arg):
        
        # keepends keep the newlines
        keepends=0 # set to True to keep newlines
        line_process = arg.splitlines(keepends)
        return line_process
        
    def anim_setup(self,cursor_default,FPS_default):
        
        # try and do something here to 
        if self.cursor_override == None:
            # set cursor to cursor_def
            if cursor_default == 'visible':
                self.cursor_visible()
            elif cursor_default == 'invisible':
                self.cursor_invisible()
        else:
            self.set_cursor()
            
        # set frame-rate depending on the length of the text
        # 25 
        #self.debug(str(self.txtlen))
        if self.FPS_override == None:
            self.FPS=FPS_default #+(self.txtlen/8) 
        else:
            self.FPS = self.FPS_override
        
        self.timer('go') 
        
    def do_newline(self):
        
        self.txtpos=1
        #self.initpos=1 # margins work with txtfx6
        self.spinpos=1
        self.colpos=0     # used for colour cycling the spinner
        self.txtcolpos=0  # used for colour cycling the text
        self.spinanim=0   # ?
        self.spsw=0          # 0 is off, 1 -7 are different types
        self.txtfxpos=0         # for matrix effect
        self.txt= []              # arg string that needs to be reset or it appends to the last string...
        self.shuffle_array= []  # for shuffle matrix effect
        #self.txtfxinitpos = 0
        self.txtlen = 0
        self.txtpos = 0
        self.txtpos = 0
        
        #self.txt=' '.join(self.txt)
        #self.txtlen = len(self.txt)
        #self.shuffle_array = self.shuffle(self.txt)    
        self.cap_array = []
        self.word_array = []
        
        self.duh=0
        self.duh2=0
        self.num1=0
        self.num2=0    
        
        #self.word_anim=0 # word.matrix
        #self.word=''
        
        self.startline += 1
        self.currentattrs = [] # do we need this ?
        self.attrspace = []
        
        #do the newline
        #stdout.write('\x1b[0m' + '\n') 
        stdout.write('\n') 

    def do_wordspace(self):
        
        if self.typefx != 4: # dont use word spaces for shuffle array cos it contains the spaces already
            # otherwise put a space at the end of the word
            stdout.write ('\033[%dG'%self.txtpos + ' ')
            self.txtpos +=1
            
    def print_out(self,x,y,colour,letter):
        
        # some kind of thread lock here ????
        #attrs = []
        stdout.write('\033[%d;%dH'%(x,y) + colour + letter)

    def txt_cycle (self):

        if self.txtcycle:
            blah = [reset]
            tmpword = colist1[self.txtcolpos]
            blah.append(format % (colours[tmpword]+fgoffset))
            self.last_colour = esc.join(blah)
            self.txtcolpos+=1
            self.txtcolpos%=len(colist1)
            
    def rainbow_cycle (self):

        if self.rainbow:
            blah = [reset]
            freq=439.9
            i=self.rainanim
            
            # rainbow calc
            red = math.sin(freq*i + 0) * 127 + 128
            green = math.sin(freq*i + 2*math.pi/3) * 127 + 128
            blue = math.sin(freq*i + 4*math.pi/3) * 127 + 128
            
            answer = colourspace.RGB2ansi(red,green,blue)
            
            blah.append(format256 % (answer))
            self.colour = esc.join(blah)
            self.rainanim += 1
            return self.colour
            

    def invert_caps(self,array):

        return array.swapcase()

    def shuffle(self,array):

        # returns numbered shuffled list  - string has each character separated out and numbered
        array_process = list((i,w) for i,w in enumerate(array))
        random.shuffle(array_process)
        return array_process

    def wordmatrix (self):        # typefx 6
        # ++++ Variables ++++
        # letterfx = random letter choice for scrolly grey faded matrix thinger
        # self.txtfxpos 
        # self.txtpos
        # self.txtlen
        # self.txt
        # tmppos - local variable for iteration...

        # self.wod_anim = word iterator
        # debugging crap
        if DEBUG == 'ON':
            self.debug(' self.word_anim:' + str(self.word_anim) + ' self.word:' + str(self.word) +\
            ' self.word_anim:' + str(self.word_anim) + '\n')

            
        tmppos = self.word[self.word_anim][0] 
        # colourspace errors if you dont minus the init pos - cos of txtpos has the initpos added automatically for some reason somewhere
        stdout.write('\033[%d;%dH'%(self.startline,(tmppos + self.txtpos)) + self.attrspace[tmppos + self.txtpos - self.initpos] + self.colourspace[tmppos + self.txtpos - self.initpos ] + self.word[self.word_anim][1])
        stdout.flush()
        
        # debugging crap
        if DEBUG == 'ON':
            self.debug('tmppos:' + str(tmppos) + ' txtfxinitpos:' + str(self.txtfxinitpos) + ' txtpos:' + str(self.txtpos) +\
            ' self.txtlen:' + str(self.txtlen) + ' self.word_anim:' + str(self.word_anim) + '\n' )

        self.word_anim += 1

    def capsmatrix (self):        # typefx 5
    # ++++ Variables ++++
    # letterfx = random letter choice for scrolly grey faded matrix thinger
    # self.txtfxpos 
    # self.txtpos
    # self.txtlen
    # self.txt
    # a - local variable for iteration...
    # 
        if self.duh < self.txtlen:
            # start printing out shuffle_array - which is a shuffled array of the text with index numbers
            tmppos = self.shuffle_array[self.duh][0] + self.txtfxinitpos
            stdout.write('\033[%d;%dH'%(self.startline,tmppos) + self.attrspace[tmppos - self.txtfxinitpos] + self.colourspace[tmppos - self.txtfxinitpos] + self.shuffle_array[self.duh][1])
            stdout.flush()
            
            #oopspos = self.word(self.word_anim[1])  + self.txtfxinitpos -1
            #stdout.write('\033[%dG'%(oopspos) + self.colourspace[oopspos + self.txtpos]) #+ self.word[self.word_anim][1])
            #stdout.flush()
            
            #self.matrix()


            self.duh += 1
            
            # debugging crap
            if DEBUG == 'ON':
                self.debug('middle:' + str(self.middle) + 'duh:' + str(self.duh) + ' cap_index1:' + str(self.cap_index1) +\
                ' cap_index2:' + str(self.cap_index2) + ' cap_index3:' + str(self.cap_index3) +\
                ' cap_index4:' + str(self.cap_index4) + ' self.word_anim:' + str(self.word_anim) + '\n' )
                #'textlen:' + str(self.txtlen) + '\n \r')

            # inward going outward
            if self.duh < (self.txtlen*2-5):
                # every other animation switch sides
                if self.duh%2 == 0:
                    # forward
                    if self.cap_index1 < self.txtlen-1:
                        self.cap_index1 += 1
                        stdout.write('\033[%d;%dH'%(self.startline,(self.cap_index1 + self.txtfxinitpos) )  + self.attrspace[self.cap_index1] + self.colourspace[self.cap_index1]  + self.cap_array[self.cap_index1])
                        stdout.flush()
                else:
                    # backward
                    if self.cap_index2 == 0:
                        self.cap_index2 -= 1
                        stdout.write('\033[%d;%dH'%(self.startline, (self.cap_index2 + self.txtfxinitpos)) + self.attrspace[self.cap_index2] + self.colourspace[self.cap_index2]  + self.cap_array[self.cap_index2])
                        stdout.flush()

            # outward HIGHLIGHT going inward
            if self.duh > self.txtlen/4:
                if self.duh%2 == 0:
                    # backward
                    if self.cap_index3 != self.middle:
                        stdout.write('\033[%d;%dH'%(self.startline, (self.cap_index3 + self.txtfxinitpos)) + self.attrspace[self.cap_index3] + self.highlight_colour + self.cap_array[self.cap_index3]) # highlight
                        stdout.flush()
                    # forward
                    if self.cap_index4 != self.middle + 1:
                        stdout.write('\033[%d;%dH'%(self.startline, (self.cap_index4 + self.txtfxinitpos)) + self.attrspace[self.cap_index4] + self.highlight_colour + self.cap_array[self.cap_index4]) # highlight
                        stdout.flush()
                else:
                    # backward
                    if self.cap_index3 != self.middle:
                        stdout.write('\033[%d;%dH'%(self.startline, (self.cap_index3 + self.txtfxinitpos)) + self.attrspace[self.cap_index3] + self.colourspace[self.cap_index3] + self.cap_array[self.cap_index3])
                        stdout.flush()
                        self.cap_index3 -= 1 # move on to next animation
                    # forward
                    if self.cap_index4 != self.middle + 1:
                        stdout.write('\033[%d;%dH'%(self.startline, (self.cap_index4 + self.txtfxinitpos)) + self.attrspace[self.cap_index4] + self.colourspace[self.cap_index4] + self.cap_array[self.cap_index4])
                        stdout.flush()
                        self.cap_index4 += 1 # move on to next animation
            else:
                return
        elif self.duh == self.txtlen:
            # do stuff on last animation to reset colours etc...
            stdout.write('\033[%d;%dH'%(self.startline, (self.cap_index3 + self.txtfxinitpos)) + self.attrspace[self.cap_index3] + self.colourspace[self.cap_index3] + self.cap_array[self.cap_index3]) # highlight reset
            stdout.write('\033[%d;%dH'%(self.startline, (self.cap_index4 + self.txtfxinitpos)) + self.attrspace[self.cap_index4] + self.colourspace[self.cap_index4] + self.cap_array[self.cap_index4]) # highlight reset
            stdout.flush()
        return

    def shufflematrix (self):        # typefx 4
        # ++++ Variables ++++
        # letterfx = random letter choice for scrolly grey faded matrix thinger
        # self.txtfxpos 
        # self.txtpos
        # self.txtlen
        # self.txt
        # a - local variable for iteration...
        #     
            # debugging crap
            #if DEBUG == 'ON':
            #    self.debug('duh:' + str(self.duh) +  \
            #    ' shuffle_array:' + str(self.shuffle_array) +\
            #    ' txtfxinitpos:' + str(self.txtfxinitpos) + '\n' +\
            #    ' txtpos:' + str(self.txtpos) + '\n' +\
            #    'textlen:' + str(self.txtlen) + '\n')
            # if we're done return
        if self.duh < self.txtlen:
            # WE NEED ALL POSITIONS WITHIN HAT WORD NOT LIKE THIS....
            tmppos = self.shuffle_array[self.duh][0] + self.txtfxinitpos
            self.debug('\n tmppos:' + str(tmppos))
            stdout.write('\033[0m\033[%d;%dH'%(self.startline, tmppos) + self.attrspace[(self.shuffle_array[self.duh][0])] + self.colourspace[tmppos - self.txtfxinitpos] + self.shuffle_array[self.duh][1])
            stdout.flush()
            #self.matrix()
                

    def matrix (self):            # typefx 3

    # ++++ Variables ++++
    # letterfx = random letter choice for scrolly grey faded matrix thinger
    # self.txtfxpos 
    # self.txtpos
    # self.txtlen
    # self.txt
    # a - local variable for iteration...
    # 
        for a in range(0,24):
            letterfx = random.choice('90!@#$%^&*()_+=-[]\|}{;\'":./,<>?`~')
            
            if self.txtfxpos+a < self.txtlen and a%2 == 0:
                
                if self.txt[self.txtfxpos + a]  != ' ':
                    
                    blah = [reset]
                    greyscale_fade = 231 + a # this makes it be white at the far right end
                    #greyscale_fade = 255 - a # this makes it be white at far left end
                    blah.append(format256 % greyscale_fade)
                    self.highlight_colour = esc.join(blah)
                    # alternate 
                    rndx = random.randrange(0,2)
                    if rndx == 0:
                        
                        tmppos = int(self.txtfxinitpos + self.txtfxpos + a )

                        stdout.write('\033[%d;%dH'%(self.startline, tmppos) + self.attrspace[self.txtfxpos] + self.highlight_colour + letterfx)
                        stdout.flush()

                    else:
                        if self.txtfxpos > 0:
                            stdout.write('\033[%d;%dH'%(self.startline,(self.txtfxinitpos + self.txtfxpos )) + self.attrspace[self.txtfxpos] + self.colourspace[self.txtfxpos] + self.txt[self.txtfxpos])
                            stdout.flush()
                            pass

            #elif self.txtpos < self.txtlen/2:
                #pass
                #stupidpos = self.shuffle_array[self.txtfxpos][0] + self.txtfxinitpos
                #if stupidpos > self.txtfxpos:
                #    stdout.write('\x1b[38;5;236m' + '\033[%dG'%stupidpos + self.shuffle_array[self.txtfxpos][1])
            # write real letter at end of garbage
            if self.txtfxpos < self.txtlen:
                stdout.write('\033[%d;%dH'%(self.startline, (self.txtfxinitpos + self.txtfxpos)) + self.attrspace[self.txtfxpos] + self.colourspace[self.txtfxpos] + self.txt[self.txtfxpos])
                stdout.flush()
            
        self.txtpos += 1
        self.txtfxpos += 1
        
        return

    def run (self):

        # effects stuff
        self.num1=0
        self.num2=0    

        self.cursor="_"
        
        # animation clocks
        self.duh=0
        self.duh2=0
        
        # newline count
        newline=0
        
        # split the string into lines
        self.lines = self.process_lines(self.arg)
        #self.debug('HELLO here is the original self.arg: \n' + self.arg + '\n\n')
        
        # g0 through each newline
        for x,woo in enumerate(self.lines):
            #self.debug ( 'now we are going through each line of the self.lines: \n' + str(x) + woo + '\n')
            
            if newline ==0 or newline < x:
                
                testes = woo # gets rid of space around text
                
                self.debug ( str(x) + testes + '\n')

                # process string and arguments
                self.process(testes)

                # test if spinner is wanted and set the text position to be moved across a bit to allow for it
                if self.spsw != 0:
                    self.txtpos = (4+self.initpos)
                    self.spinpos = self.initpos
                    self.txtfxinitpos = (4+self.initpos)
                else:
                    self.txtpos= self.initpos
                    self.txtfxinitpos= self.initpos
                    self._stop=True
            
                # caps matrix stuff
                self.middle = int(self.txtlen/2) + 1
                self.cap_index1 = self.middle 
                self.cap_index2 = self.middle - 1
                self.cap_index3 = self.txtlen - 1 
                self.cap_index4 = 0
            
                # word matrix stuff
                self.word_anim=0

                # go through each entry in self.arg_process 
                for word in self.arg_process:
                    # x is False / text
                    if word[0] is False:
                        # dont be silly
                        #textblerp = random.choice('0123456')
                        #self.typefx = textblerp
                        if self.typefx == 6:
                            # ----WORD MATRIX----
                            self.anim_setup(cursor_default='visible',FPS_default=15) # change this so it doesnt run every word.
                            self.word_anim = 0
                            self.word = self.shuffle(word[1])
                            wordlen = len(self.word)
                        
                            # main loop
                            for letter in word[1]:
                                #self.txt_cycle() # choose a colour if text cycle is on
                                self.wordmatrix() # animate bitch
                                self.timer() # pause so that the animation runs at self.FPS
                                self.spin_advance(self.FPS/7) # advance spinner every x frames
                                
                            self.txtpos += wordlen
                            
                            # debugging crap
                            if DEBUG == 'ON':
                                self.debug('wordlen:' + str(wordlen) + ' self.word_anim:' + str(self.word_anim) + ' self.word:' + str(self.word) +\
                                ' self.word_anim:' + str(self.word_anim) + ' wordlen:' + str(wordlen)  + '\n')

                        elif self.typefx == 5:
                            # ----CAPS MATRIX----
                            self.anim_setup(cursor_default='invisible',FPS_default=30)
                            self.word_anim=0
                            self.word = self.shuffle(word[1])
                            wordlen = len(self.word)
                            
                            
                            for letter in word[1]:
                                self.capsmatrix()
                                self.timer() # pause so that the animation runs at self.FPS
                                self.spin_advance(2)
                                self.txtpos +=1
                                
                            
                            self.word_anim=0
                            
                            if self.arg_process[-1][1] == word[1]:
                                for wtf in range (0, self.txtlen//4):
                                    self.capsmatrix()
                                    self.timer() # pause so that the animation runs at self.FPS
                                    self.spin_advance(2)
                                    self.txtpos +=1
                                    self.word_anim+=1
                            
                        elif self.typefx == 4:
                            # ----SHUFFLE MATRIX----
                            self.anim_setup(cursor_default='invisible',FPS_default=30)
                            
                            # print out the words letter by letter
                            for letter in word[1]:
                                self.debug('\nLETTERRRRRRRRRRRRRRRRRRRRR' + str(letter) + '\n\n\n')
                                #self.txt_cycle()
                                self.shufflematrix()
                                self.timer() # pause so that the animation runs at self.FPS
                                #self.matrix()
                                self.spin_advance(2)
                                self.duh += 1
                            self.shufflematrix()
                            #self.matrix()
                            self.duh += 1
                            
                        elif self.typefx == 3: 
                            # ---- MATRIX ----
                            self.anim_setup(cursor_default='invisible',FPS_default=40)
                            # WORD MATRIX TEST RIP OFF
                            self.word = self.shuffle(word[1])
                            self.word_anim = 0
                            self.wordlen = len(self.word)
                            # print out the words letter by letter
                            for letter in word[1]:
                                self.matrix()
                                self.timer() # pause so that the animation runs at self.FPS
                                #self.capsmatrix()
                                self.spin_advance(2)
                            if self.arg_process[-1][1] == word[1]:
                                for wtf in range (0, self.txtlen//4):
                                    self.matrix()
                                    self.timer() # pause so that the animation runs at self.FPS
                                    #self.capsmatrix()
                                    self.spin_advance(2)
                                    
                        elif self.typefx == 2: 
                            # ---- DEFAULT TYPING EFFECT ---- type is on and set to 'letter'
                            self.anim_setup(cursor_default='invisible',FPS_default=30)
                            
                            # print out the words letter by letter
                            for letter in word[1]:
                                # THIS IS WRONG - self.txtpos should be the counter for words - sort out variables a bit more
                                stdout.write('\033[%d;%dH'%(self.startline,self.txtpos) + self.attrspace[self.txtpos-self.txtfxinitpos] + self.colourspace[self.txtpos-self.txtfxinitpos] + letter)
                                #self.print_out(self.startline,self.txtpos,self.colourspace[self.txtpos-self.txtfxinitpos],letter)
                                stdout.flush()
                                self.spin_advance(2)
                                self.timer() # pause so that the animation runs at self.FPS
                                self.txtpos +=1
                        
                        elif self.typefx == 1:
                            # __ WORD BY WORD -- type is on and set to word by word
                            self.anim_setup(cursor_default='invisible',FPS_default=30)
                            
                            #self.txt_cycle()
                            
                            # go through the letters to correctly display the colourspace - and then flush by word
                            for y,w in enumerate(word[1]):
                                stdout.write('\033[%d;%dH'%(self.startline,(self.txtpos+y)) + self.attrspace[self.txtpos+y - self.txtfxinitpos] + self.colourspace[self.txtpos+y - self.txtfxinitpos] + w)
                            stdout.flush()
                            self.txtpos += len(word[1])
                            time.sleep(0.1)
                            stdout.flush()
                            self.spin_advance(self.FPS/7)
                                        
                        else: # type is off
                            self.anim_setup(cursor_default='visible',FPS_default=999)
                            #self.txt_cycle()
                            for y,w in enumerate(word[1]):
                                stdout.write('\033[%d;%dH'%(self.startline,(self.txtpos+y)) + self.attrspace[self.txtpos+y-self.txtfxinitpos] + self.colourspace[self.txtpos+y-self.txtfxinitpos] + w)
                            stdout.flush()
                            self.txtpos += len(word[1])
                            self.spin_advance(self.FPS/7)
                            
                        # only do wordspace for certain algos    
                        self.do_wordspace()
            
                    # x is True / command
                    else:
                        # allow for empty commands (re: spinner objects) - unless teh spinner command can skip tuples in the process ???
                        # if the second value in the tuple has something in it, test it....
                        # DEAL WITH THIS IN PROCESS

                        if word[1] == 'txtcycle':
                            self.txtcycle = not self.txtcycle
                        elif word[1] :
                            #stdout.write(word[2]) # attributes - this might be blerped off 
                            stdout.write(word[1]) # if theres an escape seq write it
                            stdout.flush()
                    
                        
                        
                #self.debug('HELLO here is the self.arg_process at the end: \n' + str(self.arg_process) + '\n\n')
                newline=x
                self.do_newline()

        self.timer('go')
        if self.spsw is False:
            self.stop() # sort this out ffs
        while not self._stop:
            self.cursor_invisible()
            #self.txt_cycle()
            self.spin_advance(self.FPS/7)
            self.timer()

##########################++++++++++####################+++++ MAIN +++++#############

if __name__ == '__main__':
    
    print ("You're doing it WRONG!")   

##########################++++++++++####################+++++ END +++++#############
