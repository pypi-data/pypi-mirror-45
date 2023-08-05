# -*- coding: utf-8 -*-
import logging
import string

import PyICU
import regex


def get_graphemes(in_string):
  """ Split a devanAgarI and possibly other strings into graphemes.
  
  Example: assert syllabize.get_graphemes(u"बिक्रममेरोनामहो") == "बि क् र म मे रो ना म हो".split(" ")
  :param in_string: 
  :return: 
  """
  break_iterator = PyICU.BreakIterator.createCharacterInstance(PyICU.Locale())
  break_iterator.setText(in_string)
  i = 0
  graphemes = []
  for j in break_iterator:
    s = in_string[i:j]
    graphemes.append(s)
    i = j
  return graphemes


def get_syllables(in_string):
  """ Split devanAgarI string into syllables. Ignores spaces and puncutation.
  
  syllabize.get_syllables(u"बिक्रममेरोनामहो") == "बिक् र म मे रो ना म हो".split(" ")
  :param in_string: 
  :return: 
  """
  # Cannot do \P{Letter} below as it does not match mAtra-s and virAma-s as of 2019.
  in_string = regex.sub(r"\P{Devanagari}", "", in_string, flags=regex.UNICODE)
  in_string = regex.sub(r"\p{Separator}|\p{Number}|\p{Punctuation}|\p{Other}", "", in_string, flags=regex.UNICODE)
  graphemes = get_graphemes(in_string)
  syllables = []
  while len(graphemes) > 0:
    current_syllable = graphemes.pop(0)
    while len(graphemes) > 0 and graphemes[0].endswith("्"):
      current_syllable = current_syllable  + graphemes.pop(0)
    syllables.append(current_syllable)
  return syllables

def get_maatraas(in_string):
  raise NotImplemented