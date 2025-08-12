#!/usr/bin/env python3
import sys
sys.path.append('../')
import manager as txt

import time
import random

# Delay speed (in seconds)
delay_speed = 0.9

# List of text strings to test
test_strings = [
    "Hello, World!",
    "This is a test string.",
    "Testing 123...",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "The quick brown fox jumps over the lazy dog.",
    "All your base are belong to us.",
    "01234567890abcdefghijklmnopqrstuvwxyz"
]

# Options to turn off specific sections
test_typefx = True
test_colors = True
test_misc = True
test_spinners_bullets = True
test_positioning = True

# Run the test
if test_typefx:
    for typefx in range(6):
        print(f"Testing typefx{typefx} commands...")
        txt.eko("@@")  # Clear the screen
        for test_string in test_strings:
            txt.eko(f"@typefx{typefx} {test_string}")
            time.sleep(delay_speed)  # Adjust the delay as needed
            txt.eko("@@")  # Clear the screen
            print(f"Testing typefx{typefx} commands...")

if test_colors:
    print("Testing color commands...")
    for typefx in range(6):
        txt.eko("@")  # Clear the screen
        for color in ["@red", "@green", "@blue", "^yellow", "^cyan", "^magenta", "@C123", "@C245"]:
            for test_string in test_strings:
                txt.eko(f"@typefx{typefx} {color} {test_string}")
                time.sleep(delay_speed)  # Adjust the delay as needed
                txt.eko("@@")  # Clear the screen
                print("Testing color commands...")

if test_misc:
    print("Testing miscellaneous commands...")
    for typefx in range(6):
        txt.eko("@@")  # Clear the screen
        for misc in ["@rndcase", "@txtcycle", "@spincycle"]:
            for test_string in test_strings:
                txt.eko(f"@typefx{typefx} {misc} {test_string}")
                time.sleep(delay_speed)  # Adjust the delay as needed
                txt.eko("@@")  # Clear the screen
                print("Testing miscellaneous commands...")

if test_spinners_bullets:
    print("Testing spinner and bullet point commands...")
    for typefx in range(6):
        txt.eko("@@")  # Clear the screen
        for spinner_bullet in ["@[b1]", "@[b2]", "@[b3]", "@[1]", "@[2]", "@[3]", "@[4]", "@[5]", "@[6]", "@[7]", "@[8]"]:
            for test_string in test_strings:
                txt.eko(f"@typefx{typefx} {spinner_bullet} {test_string}")
                time.sleep(delay_speed)  # Adjust the delay as needed
                txt.eko("@@")  # Clear the screen
                print("Testing spinner and bullet point commands...")

if test_positioning:
    print("Testing positioning commands...")
    txt.eko("@@")  # Clear the screen
    for test_string in test_strings:
        for position in ["@1;1", "@5;10", "@20;1", "@;5", "@", "@@"]:
            txt.eko(f"{position} {test_string}")
            time.sleep(delay_speed)  # Adjust the delay as needed
            txt.eko("@@")  # Clear the screen
            print("Testing positioning commands...")

print("Test completed.")