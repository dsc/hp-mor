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
from pprint import pprint
from collections import Counter
import yaml

# dirs
DIRS = 'etc txt counts'.split(' ')
for d in DIRS:
    globals()[d.upper()] = path(d)

# ensure
for d in (DIRS + 'counts/words counts/dialogue'.split(' ')):
    try:
        path(d).makedirs()
    except OSError: pass

def get_lines(p):
    with p.open('rU') as f:
        return f.read().strip().split('\n')

def printf(s):
    sys.stdout.write(s)
    return s




CHARACTERS = get_lines(ETC/'characters.txt')

CHAPTER_PAT = re.compile(r'chapter-(\d+)\.(?:txt|html)')
WORDS_PAT = re.compile(r"([\w']*)\s*(" + '|'.join(CHARACTERS) + r")(?:'s)?\s*([\w']*)", re.I)

opt_words = '(' + '|'.join(get_lines(ETC/'said-words.txt')) + ')?'
SAID_PAT = re.compile(opt_words+r"\s*(" + '|'.join(CHARACTERS) + r")(?:'s)?\s*"+opt_words, re.I)


def dirfiles(dir_path, glob_pat="*"):
    "Wrapper around walking files in a directory."
    for p in path(dir_path).glob(glob_pat):
        with p.open('rU') as f:
            txt = f.read()
        yield (p, txt)


from argparse import ArgumentParser

class Script(object):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version='.'.join(map(str,__version__)))
    
    def __init__(self, *args, **options):
        self.args    = args
        self.options = options
        # if not (self.args or self.options):
        #     self.parser.error("You must supply arguments or some shit!")
    
    def getNum(self, p):
        try:
            return int(CHAPTER_PAT.search(p).group(1))
        except:
            print('Unable to extract chapter number from %r' % p)
            raise
    
    
    def count_words(self):
        totals = Counter()
        
        for p, txt in dirfiles(TXT, '*.txt'):
            chapter = Counter()
            i = self.getNum(p)
            
            printf("Counting words for chapter %s... " % i)
            
            for m in WORDS_PAT.findall(txt):
                m = [ word.lower() for word in m if word ]
                try:
                    chapter.update(m)
                    totals.update(m)
                except:
                    print "Chapter %i!"
                    pprint(chapter)
                    print "---"
                    pprint(m)
                    raise
            
            with (COUNTS/'words/chapter-{:>02}.txt'.format(i)).open('w') as out:
                for pair in chapter.most_common():
                    out.write('%s: %s\n' % pair)
            
            printf("ok\n")
        
        printf("Writing counts/words/totals.txt... ")
        with (COUNTS/'words/totals.txt').open('w') as out:
            for pair in totals.most_common():
                out.write('%s: %s\n' % pair)
        printf("ok\n")
        
        return 0
    
    def __call__(self):
        return self.count_words()
    
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


