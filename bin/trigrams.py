#!/usr/bin/env python
# encoding: utf-8
"""
trigrams.py -- Tallys HP:MoR trigrams.

Script assumes a few things:

1. You've scraped all the chapters into individual files and then 
extracted only the chapter text, placing each in:

    txt/chapter-XX.txt

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
for d in (DIRS + 'counts/trigrams'.split(' ')):
    try:
        path(d).makedirs()
    except OSError: pass

def get_lines(p):
    with p.open('rU') as f:
        return f.read().strip().split('\n')

def printf(s):
    sys.stdout.write(s)
    return s

MOST_COMMON_WORDS = re.compile(r'(?:^|\s)(?:the|be|of|and|a|in|to|have|it|for|i|that|you|he|on|with|do|at|by|not|this|but|from|they|she)(?:\s|$)')

CHAPTER_PAT = re.compile(r'chapter-(\d+)\.(?:txt|html)')
STRIP_PAT = re.compile(r'[^\w\s\'_-]')
SPLIT_PAT = re.compile(r'\s+')
HTML_CONTENT_PAT = re.compile(r'<([a-zA-Z]+)[^>]*?>(.+?)</\1>')
HTML_NOCONTENT_PAT = re.compile(r'<[a-zA-Z]+[^>]*?>')

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
    
    def count_trigrams(self):
        totals = Counter()
        uc_totals = Counter()
        
        for p, txt in dirfiles(TXT, '*.txt'):
            chapter = Counter()
            uc_chapter = Counter()
            i = self.getNum(p)
            
            printf("Counting word trigrams for chapter %s " % i)
            
            txt = HTML_CONTENT_PAT.subn(r'\2', txt)[0]
            txt = HTML_NOCONTENT_PAT.subn(" ", txt)[0]
            txt = STRIP_PAT.subn(" ", txt)[0]
            words = SPLIT_PAT.split( txt.strip().lower() )
            printf("(%i words)... " % len(words))
            
            for n in range(0, len(words)-3):
                trigram = ' '.join(words[n:n+3])
                chapter[trigram] += 1
                totals[trigram] += 1
            
            uc_txt = MOST_COMMON_WORDS.subn(' ', txt)[0]
            words = SPLIT_PAT.split( uc_txt.strip().lower() )
            printf("(%i uncommon words)... " % len(words))
            
            for n in range(0, len(words)-3):
                trigram = ' '.join(words[n:n+3])
                uc_chapter[trigram] += 1
                uc_totals[trigram] += 1
            
            with (COUNTS/'trigrams/chapter-{:>02}.txt'.format(i)).open('w') as out:
                for pair in chapter.most_common(): # sorted
                    out.write('%s: %s\n' % pair)
            
            with (COUNTS/'trigrams/uc_chapter-{:>02}.txt'.format(i)).open('w') as out:
                for pair in uc_chapter.most_common(): # sorted
                    out.write('%s: %s\n' % pair)
            
            printf("ok\n")
        
        printf("Writing counts/trigrams/totals.txt... ")
        with (COUNTS/'trigrams/totals.txt').open('w') as out:
            for pair in totals.most_common():
                out.write('%s: %s\n' % pair)
        printf("ok\n")
        
        printf("Writing counts/trigrams/uc_totals.txt... ")
        with (COUNTS/'trigrams/uc_totals.txt').open('w') as out:
            for pair in uc_totals.most_common():
                out.write('%s: %s\n' % pair)
        printf("ok\n")
    
    def __call__(self):
        self.count_trigrams()
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


