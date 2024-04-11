# no licence, ***** that ***** *** ************* ****.
this program will only support 256 colour enabled terminals.

## TERM types that support 256 colours
- Eterm-256color
- gnome-256color
- konsole-256color
- putty-256color
- rxvt-256color
- screen-256color
- screen-256color-bce
- screen-256color-bce-s
- screen-256color-s
- xterm-256color
- xterm+256color

## Anatomy of a Colour Code
The general structure of a colour code is:
`echo -e "\x1b[38;5;3m hello, world"`

```
code            :: ^[[(value)m
value           :: (attributes);(foreground);(background)
attributes      :: attribute;attributes
attribute       :: 00|01|03|04|05|07|22|23|24|25|27
foreground      :: 38;05;colour
background      :: 48;05;colour
colour          :: 000-255
```

## Attribute codes
```
Reset           ::00
Bold            ::01
Italic          ::03
Underline       ::04
Blink           ::05
Reverse         ::07
No Bold         ::22
No Italic       ::23
No Underline    ::24
No Blink        ::25
No Reverse      ::27
```

## Full list
(Insert your full list here, formatted similarly to the sections above)

## Commands:
```
@x;y           : go to x,y
@;y            : go to y             # dunt werk yet
@              : go to 1;1
@@             : clear screen and go to 1;1

@[colour]      : set foreground colour
^[colour]      : set background colour
@C[0-255]      : set 256 colour number

@rndcase       : set random case - calling twice toggles
@txtcycle      : set random colour cycling for text - calling twice toggles
@spincycle     : set random colour cycling for spinner - calling twice toggles

@[b1]          : set bullet point 1-3
@[1]           : spinner on spinner type 1-8

@cursoron      : cursor visible 
@cursoroff     : cursor invisible

@typefx0       : no typing effect
@typefx1       : word by word typing effect
@typefx2       : default typing effect - left to right type
@typefx3       : matrix effect
@typefx4       : shuffle matrix effect
@typefx5       : caps matrix effect - nice one - have to work out colours for this
@typefx6       : word matrix effect

@FPS[20]       : frames per sec override - spinner must be fps divided by summat eventually 
```

## Colours:
```
{'blue': 4, 'grey': 0, 'yellow': 3, 'green': 2, 'cyan': 6, 'magenta': 5, 'white': 7, 'red': 1}
```

## Acknowledgements:
- thnx to djrevmoon, thc, stackoverflow, shawn chin, com4, aix, jsbueno, nadia almiri
- these websites were helpful:
  - www.calmar.ws/vim/256-xterm-24bit-rgb-color-chart.html
  - http://www.askapache.com/linux/zen-terminal-escape-codes.html
  - https://en.wikipedia.org/wiki/ANSI_escape_code # excellent detailed list
  - https://en.wikipedia.org/wiki/Control_character
  - www.stackoverflow.com # brilliant resource for condescending programmers and overzealous mods.
```
