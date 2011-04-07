#!/usr/bin/env python
# encoding: utf-8
"""
words.py -- Attempts to figure out synonyms for "said" to detect HP:MoR dialogue lines.

Script presumes you've scraped all the chapters into individual files and then 
extracted only the chapter text, placing each in:

    txt/chapter-XX.txt

In my files, I also removed all the paragraph markup, though that was just for
my sanity -- it won't effect the counts.

Requires: Python 2.6+, argparse, path.py

Note: chapter 64 has some unicode bullshit in it that I think I had to remove by
hand. Be warned if you scrape it yourself.
"""

__author__    = 'David Schoonover <dsc@less.ly>'
__version__   = (0, 0, 1)

import sys, re
from path import path
from argparse import ArgumentParser
from pprint import pprint
from collections import Counter

CHARACTERS = "harry hermione draco quirrell dumbledore mcgonagall neville snape".split(' ')
SAID_WORDS = 'replied quietly followed politely cried pressed screamed winced snarled sheathed shrugged imagined drawled spoke needed rose answered scowled spat resumed returned puzzled read offered laughed frowned hoped squeaked repeated hesitated suspected continued coughed reassured shouted sighed chuckled trailed warned guessed supposed swallowed called ignored talked says giggled roared angled paused say decided echoed allowed slumped forced stumbled said hissed wondered groaned gestured reminded remembered swore honestly snorted inclined announced told whispered added swayed gritted flinched blinked protested smiled snapped choked suggested figured sniggered considered invited studied grinned finished demanded dared thought gasped assumed breathed asked'.split(' ')

CHAPTER_PAT = re.compile(r'chapter-(\d+)\.txt')
WORDS_PAT = re.compile(r"([\w']*)\s*(" + '|'.join(CHARACTERS) + r")(?:'s)?\s*([\w']*)", re.I)

SAID_WORDS_PAT = '|'.join(SAID_WORDS)
SAID_PAT = re.compile(r"("+SAID_WORDS_PAT+r")?\s*(" + '|'.join(CHARACTERS) + r")(?:'s)?\s*("+SAID_WORDS_PAT+r")?", re.I)

# ensure dirs we'll look in do exist
for p in 'counts txt'.split(' '):
    try:
        path('counts').makedirs()
    except OSError: pass

class Script(object):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version='.'.join(map(str,__version__)))
    
    
    
    def __init__(self, *args, **options):
        self.args    = args
        self.options = options
        # if not (self.args or self.options):
        #     self.parser.error("You must supply arguments or some shit!")
    
    def __call__(self):
        return self.count_words() or self.count_characters()
    
    def count_characters(self):
        characters_all = Counter()
        
        for p in path('txt/').glob('*.txt'):
            characters = Counter()
            i = int(CHAPTER_PAT.search(p).group(1))
            
            sys.stdout.write("Counting lines by character for chapter %s... " % i)
            
            with p.open('rU') as f:
                txt = f.read()
            
            for m in SAID_PAT.findall(txt):
                who = m[1].lower()
                if not (m[0] or m[2]):
                    continue
                
                try:
                    characters[who] += 1
                    characters_all[who] += 1
                except:
                    print "chapter %i!"
                    pprint(characters)
                    print "---"
                    pprint(m)
                    raise
            
            with path('counts/characters-{:>02}.txt'.format(i)).open('w') as out:
                for pair in characters.most_common():
                    word, n = pair
                    if word in CHARACTERS:
                        out.write('%s: %s\n' % pair)
            
            sys.stdout.write("ok\n")
        
        sys.stdout.write("Writing characters-all.txt... ")
        with path('counts/characters-all.txt').open('w') as out:
            for pair in characters_all.most_common():
                out.write('%s: %s\n' % pair)
        sys.stdout.write("ok\n")
        
        return 0
    
    def count_words(self):
        words_all = Counter()
        
        for p in path('txt/').glob('*.txt'):
            words = Counter()
            i = int(CHAPTER_PAT.search(p).group(1))
            
            sys.stdout.write("Counting words for chapter %s... " % i)
            
            with p.open('rU') as f:
                txt = f.read()
            
            for m in WORDS_PAT.findall(txt):
                m = [ word.lower() for word in m if word ]
                try:
                    words.update(m)
                    words_all.update(m)
                except:
                    print "chapter %i!"
                    pprint(words)
                    print "---"
                    pprint(m)
                    raise
            
            with path('counts/words-{:>02}.txt'.format(i)).open('w') as out:
                for pair in words.most_common():
                    word, n = pair
                    if word not in CHARACTERS:
                        out.write('%s: %s\n' % pair)
            
            sys.stdout.write("ok\n")
        
        sys.stdout.write("Writing words-all.txt... ")
        with path('counts/words-all.txt').open('w') as out:
            for pair in words_all.most_common():
                out.write('%s: %s\n' % pair)
        sys.stdout.write("ok\n")
        
        return 0
    
    def __repr__(self):
        return '{self.__class__.__name__}(args={self.args!r}, options={self.options!r})'.format(self=self)
    
    def __str__(self):
        return repr(self)
    
    @classmethod
    def parse(Script, *args, **values):
        args = list(args)
        if values:
            for k,v in values.iteritems():
                args.append( ('--%s' % k, str(v)) )
        parsed = Script.parser.parse_args(args=args or None)
        return Script(**parsed.__dict__)



if __name__ == '__main__':
    main = Script.parse()
    sys.exit(main())


