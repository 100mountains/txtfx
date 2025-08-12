# animation_engine.py
import threading
import time
import random
import math
from sys import stdout
from constants import *
import rgb2ansi

DEBUG="OFF"

class AnimationEngine(threading.Thread):
    def __init__(self, config):
        super(AnimationEngine, self).__init__()
        self._stop = False
        self.name = "_txtfx_"
        self.config = config
        self.lines = []
        self.startline = 0
        self.cursave = '\033[s'
        self.curload = '\033[u'
        self.curup = '\033[%dA'
        self.cursor_override = None
        self.FPS = 30
        self.FPS_override = None
        self.last_time = None
        self.new_time = None
        self.spincolour = '\x1b[1;32m'
        self.highlight_colour = '\x1b[38;5;255m'
        self.last_colour = ''
        self.colour = self.last_colour
        self.colourspace = []
        self.rev_colourspace = []
        self.attrcodes = ''
        self.currentattrs = list()
        self.attrspace = []
        stdout.write('\033[0m')
        self.rainbow = 0
        self.rainanim = 0
        self.txtpos = 1
        self.initpos = 1
        self.spinpos = 1
        self.colpos = 0
        self.txtcolpos = 0
        self.spinanim = 0
        self.rndcase = 0
        self.spsw = 0
        self.typefx = 2
        self.spincycle = 0
        self.txtcycle = 0
        self.txtfxpos = 0
        self.txt = []
        self.shuffle_array = []

    def timer(self, go=None):
        if go == 'go':
            self.last_time = time.time()
        else:
            self.new_time = time.time()
            sleepy_time = ((1000.0 / (self.FPS * 2)) - (self.new_time - self.last_time)) / 1000.0
            if sleepy_time > 0:
                time.sleep(sleepy_time)
            self.last_time = self.new_time

    def debug(self, txt=None):
        if DEBUG == 'ON':
            fd.write(str(txt) + '\n')
            fd.flush()

    def thread_debug(self):
        self.debug("threading enumerate :%s" % threading.enumerate())
        self.debug("current thread :%s" % threading.current_thread())
        self.debug("thread count :%s" % threading.active_count())

    def set_cursor(self):
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
        stdout.write("\033[0m")

    def stopped(self):
        return self._stop == True

    def __exit__(self, type, value, traceback):
        return isinstance(value, TypeError)

    def spin_advance(self, x):
        if self.spsw != 0:
            if self.spincycle:
                blah = [reset]
                tmpword = colist[self.colpos]
                blah.append(format % (colours[tmpword] + fgoffset))
                self.spincolour = esc.join(blah)
            if self.clock_res == 1:
                stdout.write(self.spincolour + '\033[%dG' % self.spinpos + "{" + self.chars[
                    self.spinanim].decode("utf-8") + "}"),
                stdout.flush()
                self.spinanim += 1
                self.spinanim %= len(self.chars)
                self.colpos += 1
                self.colpos %= len(colist)
            if self.clock_res >= x:
                self.clock_res = 0
            else:
                self.clock_res += 1

    def esc_convert(self, w):
        word = w
        truth = word.startswith(('^', '@'))
        cmd = [reset]
        if truth:
            tmpword = word[1:]
            if tmpword in colours:
                if word.startswith('@'):
                    tmpoffset = fgoffset
                elif word.startswith('^'):
                    tmpoffset = bgoffset
                cmd.append(format % (colours[tmpword] + tmpoffset))
                self.colour = esc.join(cmd)
                return truth, None, self.colour
            if tmpword in attrs:
                if tmpword in self.currentattrs:
                    self.currentattrs.remove(tmpword)
                else:
                    self.currentattrs.append(tmpword)
                for blerp in self.currentattrs:
                    c = attrformat % attrs[blerp]
                    cmd.append(c)
                self.debug(str(self.currentattrs) + '\n\n' + str(attrs) + '\n\n')
                return truth, None, self.colour
            if tmpword in keywords:
                if tmpword == 'rndcase':
                    self.rndcase = not self.rndcase
                    return truth, None, self.colour
                if tmpword.startswith('typefx') and 0 <= int(tmpword[-1]) <= 6:
                    self.typefx = int(tmpword[-1])
                    return truth, None, self.colour
                if tmpword == 'spincycle':
                    self.spincycle = not self.spincycle
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
            if tmpword.startswith('[') and tmpword[-1] == ']':
                if tmpword[1] == 'b':
                    if 1 <= int(tmpword[2]) <= len(bpoints):
                        return False, bpoints[int(tmpword[2]) - 1], self.colour
                    else:
                        return False, word, self.colour
                if 1 <= int(tmpword[1]) <= len(spinners):
                    self.spsw = int(tmpword[1:-1])
                    self.chars = [c.encode("utf-8") for c in spinners[self.spsw - 1]]
                    return truth, None, self.colour
            if tmpword.startswith('FPS') and tmpword[3] == '[' and tmpword[-1] == ']':
                self.FPS_override = int(tmpword[4:-1])
                return truth, None, self.colour
            if tmpword.startswith('C[') and tmpword[-1] == ']':
                tmpcolour = int(tmpword[2:-1])
                cmd.append(format256 % tmpcolour)
                self.colour = esc.join(cmd)
                return truth, None, self.colour
            if tmpword == '@':
                cmd.append('2J')
                cmd.append('H')
                return truth, esc.join(cmd), self.colour
            elif ';' in tmpword:
                cmd.append('%sH' % tmpword)
                self.initpos = int(tmpword.split(';')[1])
                self.startline = int(tmpword.split(';')[0])
                return truth, esc.join(cmd), self.colour
        else:
            if self.rndcase:
                word = ''.join(random.choice((str.upper, str.lower))(x) for x in word)
            self.attrcodes = '\x1b[0m'
            for blerp in self.currentattrs:
                c = attrformat % attrs[blerp]
                self.attrcodes += c
            for t in word:
                if self.rainbow == 1:
                    self.colourspace.append(self.rainbow_cycle())
                else:
                    self.colourspace.append(self.colour)
                self.attrspace.append(self.attrcodes)
            self.debug(str(self.attrspace))
            self.colourspace.append(self.colour)
            self.attrspace.append('')
            return truth, word, self.colour

    def process(self, line):
        self.arg_process = [self.esc_convert(w) for w in line.split()]
        self.txt = []
        self.colourspace = []
        self.attrspace = []
        for i, word in enumerate(self.arg_process):
            if word[0] is False:
                self.txt.append(word[1])
                for _ in word[1]:
                    self.colourspace.append(word[2])
                    self.attrspace.append(self.attrcodes)
                self.colourspace.append(word[2])
                self.attrspace.append('')
        self.txt = ' '.join(self.txt)
        self.txtlen = len(self.txt)
        self.shuffle_array = self.shuffle(self.txt)
        self.cap_array = self.invert_caps(self.txt)
        self.word_array = list(self.txt.split())
        self.rev_colourspace = self.colourspace[::-1]
        self.debug('self.arg_process: ' + str(self.arg_process) + '\n\n')
        self.debug('self.shuffle_array: ' + str(self.shuffle_array) + '\n\n')

    def process_lines(self, lines):
        keepends = 0
        line_process = lines
        return line_process
    def anim_setup(self, cursor_default, FPS_default):
        if self.cursor_override == None:
            if cursor_default == 'visible':
                self.cursor_visible()
            elif cursor_default == 'invisible':
                self.cursor_invisible()
        else:
            self.set_cursor()
        if self.FPS_override == None:
            self.FPS = FPS_default
        else:
            self.FPS = self.FPS_override
        self.timer('go')

    def do_newline(self):
        self.txtpos = 1
        self.spinpos = 1
        self.colpos = 0
        self.txtcolpos = 0
        self.spinanim = 0
        self.spsw = 0
        self.txtfxpos = 0
        self.txt = []
        self.shuffle_array = []
        self.txtlen = 0
        self.txtpos = 0
        self.txtpos = 0
        self.cap_array = []
        self.word_array = []
        self.duh = 0
        self.duh2 = 0
        self.num1 = 0
        self.num2 = 0
        self.startline += 1
        self.currentattrs = []
        self.attrspace = []
        stdout.write('\n')

    def do_wordspace(self):
        if self.typefx != 4:
            stdout.write('\033[%dG' % self.txtpos + ' ')
            self.txtpos += 1

    def print_out(self, x, y, colour, letter):
        stdout.write('\033[%d;%dH' % (x, y) + colour + letter)

    def txt_cycle(self):
        if self.txtcycle:
            blah = [reset]
            tmpword = colist1[self.txtcolpos]
            blah.append(format % (colours[tmpword] + fgoffset))
            self.last_colour = esc.join(blah)
            self.txtcolpos += 1
            self.txtcolpos %= len(colist1)

    def rainbow_cycle(self):
        if self.rainbow:
            blah = [reset]
            freq = 439.9
            i = self.rainanim
            red = math.sin(freq * i + 0) * 127 + 128
            green = math.sin(freq * i + 2 * math.pi / 3) * 127 + 128
            blue = math.sin(freq * i + 4 * math.pi / 3) * 127 + 128
            answer = rgb2ansi.RGB2ansi(red, green, blue)
            blah.append(format256 % (answer))
            self.colour = esc.join(blah)
            self.rainanim += 1
            return self.colour

    def invert_caps(self, array):
        return array.swapcase()

    def shuffle(self, array):
        array_process = list((i, w) for i, w in enumerate(array))
        random.shuffle(array_process)
        return array_process

    def wordmatrix(self):
        if DEBUG == 'ON':
            self.debug(' self.word_anim:' + str(self.word_anim) + ' self.word:' + str(self.word) + \
                      ' self.word_anim:' + str(self.word_anim) + '\n')
        tmppos = self.word[self.word_anim][0]
        stdout.write('\033[%d;%dH' % (self.startline, (tmppos + self.txtpos)) + self.attrspace[
            tmppos + self.txtpos - self.initpos] + self.colourspace[tmppos + self.txtpos - self.initpos] + self.word[
                         self.word_anim][1])
        stdout.flush()
        if DEBUG == 'ON':
            self.debug('tmppos:' + str(tmppos) + ' txtfxinitpos:' + str(self.txtfxinitpos) + ' txtpos:' + str(
                self.txtpos) + \
                      ' self.txtlen:' + str(self.txtlen) + ' self.word_anim:' + str(self.word_anim) + '\n')
        self.word_anim += 1

    def capsmatrix(self):
        if self.duh < self.txtlen:
            tmppos = self.shuffle_array[self.duh][0] + self.txtfxinitpos
            stdout.write('\033[%d;%dH' % (self.startline, tmppos) + self.attrspace[tmppos - self.txtfxinitpos] +
                         self.colourspace[tmppos - self.txtfxinitpos] + self.shuffle_array[self.duh][1])
            stdout.flush()
            if DEBUG == 'ON':
                self.debug('middle:' + str(self.middle) + 'duh:' + str(self.duh) + ' cap_index1:' + str(
                    self.cap_index1) + \
                          ' cap_index2:' + str(self.cap_index2) + ' cap_index3:' + str(self.cap_index3) + \
                          ' cap_index4:' + str(self.cap_index4) + ' self.word_anim:' + str(self.word_anim) + '\n')
            if self.duh < (self.txtlen * 2 - 5):
                if self.duh % 2 == 0:
                    if self.cap_index1 < self.txtlen - 1:
                        self.cap_index1 += 1
                        stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index1 + self.txtfxinitpos)) +
                                     self.attrspace[self.cap_index1] + self.colourspace[self.cap_index1] +
                                     self.cap_array[self.cap_index1])
                        stdout.flush()
                else:
                    if self.cap_index2 == 0:
                        self.cap_index2 -= 1
                        stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index2 + self.txtfxinitpos)) +
                                     self.attrspace[self.cap_index2] + self.colourspace[self.cap_index2] +
                                     self.cap_array[self.cap_index2])
                        stdout.flush()
            if self.duh > self.txtlen / 4:
                if self.duh % 2 == 0:
                    if self.cap_index3 != self.middle:
                        stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index3 + self.txtfxinitpos)) +
                                     self.attrspace[self.cap_index3] + self.highlight_colour + self.cap_array[
                                         self.cap_index3])
                        stdout.flush()
                    if self.cap_index4 != self.middle + 1:
                        stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index4 + self.txtfxinitpos)) +
                                     self.attrspace[self.cap_index4] + self.highlight_colour + self.cap_array[
                                         self.cap_index4])
                        stdout.flush()
                else:
                    if self.cap_index3 != self.middle:
                        stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index3 + self.txtfxinitpos)) +
                                     self.attrspace[self.cap_index3] + self.colourspace[self.cap_index3] +
                                     self.cap_array[self.cap_index3])
                        stdout.flush()
                        self.cap_index3 -= 1
                    if self.cap_index4 != self.middle + 1:
                        stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index4 + self.txtfxinitpos)) +
                                     self.attrspace[self.cap_index4] + self.colourspace[self.cap_index4] +
                                     self.cap_array[self.cap_index4])
                        stdout.flush()
                        self.cap_index4 += 1
        elif self.duh == self.txtlen:
            stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index3 + self.txtfxinitpos)) + self.attrspace[
                self.cap_index3] + self.colourspace[self.cap_index3] + self.cap_array[self.cap_index3])
            stdout.write('\033[%d;%dH' % (self.startline, (self.cap_index4 + self.txtfxinitpos)) + self.attrspace[
                self.cap_index4] + self.colourspace[self.cap_index4] + self.cap_array[self.cap_index4])
            stdout.flush()
        return

    def shufflematrix(self):
        if self.duh < self.txtlen:
            tmppos = self.shuffle_array[self.duh][0] + self.txtfxinitpos
            self.debug('\n tmppos:' + str(tmppos))
            stdout.write('\033[0m\033[%d;%dH' % (self.startline, tmppos) + self.attrspace[
                (self.shuffle_array[self.duh][0])] + self.colourspace[tmppos - self.txtfxinitpos] +
                         self.shuffle_array[self.duh][1])
            stdout.flush()

    def matrix(self):
        for a in range(0, 24):
            letterfx = random.choice('90!@#$%^&*()_+=-[]\|}{;\'":./,<>?`~')
            if self.txtfxpos + a < self.txtlen and a % 2 == 0:
                if self.txt[self.txtfxpos + a] != ' ':
                    blah = [reset]
                    greyscale_fade = 231 + a
                    blah.append(format256 % greyscale_fade)
                    self.highlight_colour = esc.join(blah)
                    rndx = random.randrange(0, 2)
                    if rndx == 0:
                        tmppos = int(self.txtfxinitpos + self.txtfxpos + a)
                        stdout.write('\033[%d;%dH' % (self.startline, tmppos) + self.attrspace[self.txtfxpos] +
                                     self.highlight_colour + letterfx)
                        stdout.flush()
                    else:
                        if self.txtfxpos > 0:
                            stdout.write('\033[%d;%dH' % (
                            self.startline, (self.txtfxinitpos + self.txtfxpos)) + self.attrspace[self.txtfxpos] +
                                         self.colourspace[self.txtfxpos] + self.txt[self.txtfxpos])
                            stdout.flush()
            if self.txtfxpos < self.txtlen:
                stdout.write('\033[%d;%dH' % (
                self.startline, (self.txtfxinitpos + self.txtfxpos)) + self.attrspace[self.txtfxpos] +
                             self.colourspace[self.txtfxpos] + self.txt[self.txtfxpos])
                stdout.flush()
        self.txtpos += 1
        self.txtfxpos += 1
        return

    def run(self):
        self.num1 = 0
        self.num2 = 0
        self.cursor = "_"
        self.duh = 0
        self.duh2 = 0
        newline = 0
        self.lines = self.process_lines(self.config['text'])
        for x, woo in enumerate(self.lines):
            if newline == 0 or newline < x:
                testes = woo
                self.debug(str(x) + testes + '\n')
                self.process(testes)
                if self.spsw != 0:
                    self.txtpos = (4 + self.initpos)
                    self.spinpos = self.initpos
                    self.txtfxinitpos = (4 + self.initpos)
                else:
                    self.txtpos = self.initpos
                    self.txtfxinitpos = self.initpos
                    self._stop = True
                self.middle = int(self.txtlen / 2) + 1
                self.cap_index1 = self.middle
                self.cap_index2 = self.middle - 1
                self.cap_index3 = self.txtlen - 1
                self.cap_index4 = 0
                self.word_anim = 0
                for word in self.config['text']:
                    if self.typefx == 6:
                        self.anim_setup(cursor_default='visible', FPS_default=15)
                        self.word_anim = 0
                        self.word = self.shuffle(word)
                        wordlen = len(self.word)
                        for letter in word:
                            self.wordmatrix()
                            self.timer()
                            self.spin_advance(self.FPS / 7)
                        self.txtpos += wordlen
                        if DEBUG == 'ON':
                            self.debug('wordlen:' + str(wordlen) + ' self.word_anim:' + str(
                                self.word_anim) + ' self.word:' + str(self.word) + \
                                    ' self.word_anim:' + str(self.word_anim) + ' wordlen:' + str(
                                wordlen) + '\n')
                    elif self.typefx == 5:
                        self.anim_setup(cursor_default='invisible', FPS_default=30)
                        self.word_anim = 0
                        self.word = self.shuffle(word)
                        wordlen = len(self.word)
                        for letter in word:
                            self.capsmatrix()
                            self.timer()
                            self.spin_advance(2)
                            self.txtpos += 1
                        self.word_anim = 0
                        if word == self.config['text'][-1]:
                            for wtf in range(0, self.txtlen // 4):
                                self.capsmatrix()
                                self.timer()
                                self.spin_advance(2)
                                self.txtpos += 1
                                self.word_anim += 1
                    elif self.typefx == 4:
                        self.anim_setup(cursor_default='invisible', FPS_default=30)
                        for letter in word:
                            self.debug('\nLETTERRRRRRRRRRRRRRRRRRRRR' + str(letter) + '\n\n\n')
                            self.shufflematrix()
                            self.timer()
                            self.spin_advance(2)
                            self.duh += 1
                        self.shufflematrix()
                        self.duh += 1
                    elif self.typefx == 3:
                        self.anim_setup(cursor_default='invisible', FPS_default=40)
                        self.word = self.shuffle(word)
                        self.word_anim = 0
                        self.wordlen = len(self.word)
                        for letter in word:
                            self.matrix()
                            self.timer()
                            self.spin_advance(2)
                        if word == self.config['text'][-1]:
                            for wtf in range(0, self.txtlen // 4):
                                self.matrix()
                                self.timer()
                                self.spin_advance(2)
                    elif self.typefx == 2:
                        self.anim_setup(cursor_default='invisible', FPS_default=30)
                        for letter in word:
                            stdout.write('\033[%d;%dH' % (
                            self.startline, self.txtpos) + self.attrspace[self.txtpos - self.txtfxinitpos] +
                                        self.colourspace[self.txtpos - self.txtfxinitpos] + letter)
                            stdout.flush()
                            self.spin_advance(2)
                            self.timer()
                            self.txtpos += 1
                    elif self.typefx == 1:
                        self.anim_setup(cursor_default='invisible', FPS_default=30)
                        for y, w in enumerate(word):
                            stdout.write('\033[%d;%dH' % (
                            self.startline, (self.txtpos + y)) + self.attrspace[self.txtpos + y - self.txtfxinitpos] +
                                        self.colourspace[self.txtpos + y - self.txtfxinitpos] + w)
                        stdout.flush()
                        self.txtpos += len(word)
                        time.sleep(0.1)
                        stdout.flush()
                        self.spin_advance(self.FPS / 7)
                    else:
                        self.anim_setup(cursor_default='visible', FPS_default=999)
                        for y, w in enumerate(word):
                            stdout.write('\033[%d;%dH' % (
                            self.startline, (self.txtpos + y)) + self.attrspace[self.txtpos + y - self.txtfxinitpos] +
                                        self.colourspace[self.txtpos + y - self.txtfxinitpos] + w)
                        stdout.flush()
                        self.txtpos += len(word)
                        self.spin_advance(self.FPS / 7)
                    self.do_wordspace()
                newline = x
                self.do_newline()
        self.timer('go')
        if self.spsw is False:
            self.stop()
        while not self._stop:
            self.cursor_invisible()
            self.spin_advance(self.FPS / 7)
            self.timer()