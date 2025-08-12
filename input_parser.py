# input_parser.py
import re
from constants import *

class InputParser:
    @staticmethod
    def parse_command(word):
        if word.startswith('@'):
            command_type = 'attribute'
            command_value = None
            if word[1:] in attrs:
                command_value = attrs[word[1:]]
            elif word[1:] in colours:
                command_value = colours[word[1:]]
            elif word[1:] in keywords:
                command_value = word[1:]
            return True, command_type, command_value
        elif word.startswith('^'):
            command_type = 'color'
            command_value = None
            if word[1:] in colours:
                command_value = colours[word[1:]]
            return True, command_type, command_value
        else:
            return False, None, None

    @staticmethod
    def parse_input(arg):
        config = {
            'attributes': {},
            'colors': {},
            'keywords': [],
            'text': []
        }

        lines = arg.split('\n')
        for line in lines:
            words = line.split()
            for word in words:
                is_command, command_type, command_value = InputParser.parse_command(word)
                if is_command:
                    if command_type == 'attribute':
                        config['attributes'][word[1:]] = command_value
                    elif command_type == 'color':
                        config['colors'][word[1:]] = command_value
                    elif command_type == 'keyword':
                        config['keywords'].append(command_value)
                else:
                    config['text'].append(word)

        return config