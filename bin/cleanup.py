#!/usr/bin/env python
# encoding: utf-8

import sys, re
from path import path

CHAPTER_PAT = re.compile(r'chapter-(\d+)\.html')

for f in path('txt/').glob('*.html'):
    i = int(CHAPTER_PAT.search(f).group(1))
    print "Cleaning chapter %s..." % i
    with f.open('rU') as fhtml:
        html = fhtml.read()
    txt = (html
            .replace('<p>', '')
            .replace('</p>', '\n\n'))
    out = path(f.replace('.html', '.txt'))
    with out.open('w') as fout:
        fout.write(txt)
    
