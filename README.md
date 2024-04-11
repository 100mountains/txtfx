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
```
0 		Reset / Normal 	all attributes off
1 		Bright (increased intensity) or Bold 	
2 		Faint (decreased intensity) 	not widely supported
3 		Italic: on 	not widely supported. Sometimes treated as inverse.
4 		Underline: Single 	
5 		Blink: Slow 	less than 150 per minute
6 		Blink: Rapid 	MS-DOS ANSI.SYS; 150 per minute or more; not widely supported
7 		Image: Negative 	inverse or reverse; swap foreground and background
8 		Conceal 	not widely supported
9 		Crossed-out 	Characters legible, but marked for deletion. Not widely supported.
10 		Primary(default) font 	
11-19 	n-th alternate font 	Select the n-th alternate font. 14 being the fourth alternate font, up to 19 being the 9th alternate font.
20 		Fraktur 	hardly ever supported
21 		Bright/Bold: off or Underline: Double 	bold off not widely supported, double underline hardly ever
22 		Normal color or intensity 	neither bright, bold nor faint
23 		Not italic, not Fraktur 	
24 		Underline: None 	not singly or doubly underlined
25 		Blink: off 	
26 		Reserved 	
27 		Image: Positive 	
28 		Reveal 	conceal off
29 		Not crossed out 	
30-37 	Set text color 	30 + x, where x is from the color table below
38 		Set xterm-256 text color[dubious - discuss] 	next arguments are 5;x where x is color index (0..255)
39 		Default text color 	implementation defined (according to standard)
40-47 	Set background color 	40 + x, where x is from the color table below
48 		Set xterm-256 background color 	next arguments are 5;x where x is color index (0..255)
49 		Default background color 	implementation defined (according to standard)
50 		Reserved 	
51 		Framed 	
52 		Encircled 	
53 		Overlined 	
54 		Not framed or encircled 	
55 		Not overlined 	
56-59 	Reserved 	
60 		ideogram underline or right side line 	hardly ever supported
61 		ideogram double underline or double line on the right side 	hardly ever supported
62 		ideogram overline or left side line 	hardly ever supported
63 		ideogram double overline or double line on the left side 	hardly ever supported
64 		ideogram stress marking 	hardly ever supported
90-99 	Set foreground color, high intensity 	aixterm (not in standard)
100-109 	Set background color, high intensity 	aixterm (not in standard)
```

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
