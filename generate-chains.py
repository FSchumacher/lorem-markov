#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
import random
import re

def guess_encoding(in_text):
    for enc in ('utf-7', 'utf-8', 'iso-8859-1', ):
        try:
            return in_text.decode(enc)
        except Exception as e:
            pass

with file("all.txt") as f:
    text = f.read()

text = '\n'.join([guess_encoding(l) for l in text.split('\n')])

for regex, replacement in ((r'(?:\r?\n){2,}', '\n\n'), (r'\ufeff', ''), (r'\+(\w+.*\w+)\+', '\1'), ):
    text = re.sub(regex, replacement, text)

chains = {}

word_splitter = re.compile('''
    (
        \w+(?:'\w+)?    # 'normale' Woerter eventuell mit 's
        | (?:St|pp)\.   # oder St. und pp.
        | \.\.\.        # oder ...
        | [,.;:!?&-]    # oder Satzzeichen wie , oder .
    )
''', re.X | re.U)

context = ''
for word in word_splitter.findall(text):
    if context not in chains:
        chains[context] = defaultdict(int)
    chains[context][word] += 1
    context = word

def random_word(first):
    return random.choice(chains[first].keys())

def generate_sentence(first):
    result = first.capitalize()
    while True:
       if first in ('.','!', '?'):
           return result
       second = random_word(first)
       if second not in (',', ';', ':', '.', '!', '?'):
           result += ' '
       result += second
       first = second

if __name__ == '__main__':
    import sys
    try:
        num_sentences = int(sys.argv[1])
    except Exception:
        num_sentences = 5
    print "# Starte Unsinn..."
    for word in random.sample(chains.keys(), num_sentences):
        print generate_sentence(word)
