# constants.py

attrs = {'none': 0, 'bold': 1, 'faint': 2, 'fast': 6, 'blink': 5, 'concealed': 8, 'italic': 3, 'underline': 4, 'reverse': 7}

colours = dict((name, val) for val, name in enumerate('grey red green yellow blue magenta cyan white'.split()))

keywords = ['typefx0', 'typefx1', 'typefx2', 'typefx3', 'typefx4', 'typefx5', 'typefx6', 'spincycle', 'txtcycle', 'rainbow', 'rndcase', 'cursoron', 'cursoroff']

spinners = ("|/-\\", ".o0O0o.", "⇐⇖⇑⇗⇒⇘⇓⇙", "◓◑◒◐", "○◔◑◕●", "◴◷◶◵", "▏▎▍▌▋▊▉█▉▊▌▍▎", "▁▂▃▄▅▆▇█▇▆▅▄▃▂")

colist = 'grey blue cyan white cyan blue'.split()
colist1 = 'blue cyan'.split()

term_types = ['Eterm-256color', 'gnome-256color', 'konsole-256color', 'putty-256color', 'rxvt-256color',
              'screen-256color', 'screen-256color-bce', 'screen-256color-bce-s', 'screen-256color-s',
              'xterm-256color', 'xterm+256color']

esc = '\033['
reset = ''
format = '\033[0;%dm'
attrformat = '\033[%dm'
format256 = '38;5;%dm'
fgoffset, bgoffset = 30, 40