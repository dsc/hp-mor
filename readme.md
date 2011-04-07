# HP:MoR Character Dialogue Counts

As requested by the people doing the [audiobook](http://openetherpad.org/YvnjtzmvYi-EF-BB-BF), I've attempted to approximate of the number of "lines" each major character will speak.

Here's the tally for the whole story:

    harry        1385
    draco         343
    hermione      203
    dumbledore    164
    quirrell      151
    mcgonagall    105
    neville        46
    snape          11

If some of those numbers look weird (like Snape) and you're curious, read the next section. By-chapter tallys follow at the end.


## Methodology

Instead of attempting to identify each dialogue line, the script looks for a character's name preceeded or followed by a "said" word.

The [first script](bin/words.py) extracted a [giant] list of all the words that either preceeded or followed the name of a main character, and aggregated it by frequency. (The results look [like this](counts/words/totals.txt), and there are also [chapter counts](counts/words/), if you care.) I went through that list by hand to pull out words that were synonyms (for our purposes) of "said" in a dialogue line's speaking indicator, like "Harry said". (Here's [the list of words](etc/said-words.txt), and [one with counts](etc/said-counts.yaml).)

Then a [second script](bin/tally.py) went through everything again, this time only counting instances of those words preceeding or following a main character name, and keeping count by character. The totals are what you see above; the by-chapter tallys follow.

You can download a tar of all this from [github](http://github.com/dsc/hp-mor).


## By Chapter

### chapter 1
    harry        10

### chapter 2
    harry        10
    mcgonagall   6

### chapter 3
    mcgonagall   11
    harry        10

### chapter 4
    harry        10
    mcgonagall   9

### chapter 5
    harry        18
    mcgonagall   10
    draco        8

### chapter 6
    harry        50
    mcgonagall   30
    dumbledore   1

### chapter 7
    harry        50
    draco        43
    mcgonagall   1

### chapter 8
    hermione     23
    harry        3
    neville      1

### chapter 9
    harry        4

### chapter 10
    harry        7
    mcgonagall   2

### chapter 11
    dumbledore   3
    harry        1

### chapter 12
    harry        9
    dumbledore   6

### chapter 13
    harry        40
    neville      4

### chapter 14
    harry        19
    mcgonagall   13
    hermione     1

### chapter 15
    harry        12
    mcgonagall   4
    hermione     4

### chapter 16
    harry        15
    draco        12
    quirrell     10
    hermione     1

### chapter 17
    harry        87
    dumbledore   52
    draco        11
    mcgonagall   5

### chapter 18
    harry        42
    dumbledore   20
    neville      2
    hermione     2

### chapter 19
    harry        41
    quirrell     23
    draco        23

### chapter 20
    harry        38
    quirrell     26
    dumbledore   8

### chapter 21
    draco        22
    harry        13
    hermione     3

### chapter 22
    draco        24
    harry        23
    hermione     10
    dumbledore   1

### chapter 23
    harry        19
    draco        18

### chapter 24
    draco        25
    harry        22
    dumbledore   2

### chapter 25
    harry        19
    quirrell     2
    draco        1
    hermione     1

### chapter 26
    harry        37
    quirrell     15

### chapter 27
    harry        57
    neville      13
    hermione     3
    mcgonagall   1
    quirrell     1
    snape        1

### chapter 28
    harry        42
    hermione     25
    dumbledore   12
    snape        1
    mcgonagall   1

### chapter 29
    harry        32
    draco        24
    hermione     13
    quirrell     7

### chapter 30
    harry        25
    draco        10
    neville      3
    quirrell     1

### chapter 31
    hermione     4
    draco        2
    harry        2

### chapter 32
    harry        11
    quirrell     3
    dumbledore   2

### chapter 33
    harry        27
    draco        20
    hermione     7
    neville      4
    dumbledore   2

### chapter 34
    draco        9
    harry        6
    quirrell     1
    dumbledore   1

### chapter 35
    hermione     5
    harry        5
    mcgonagall   4
    quirrell     4
    draco        2
    dumbledore   1

### chapter 36
    harry        13
    hermione     3

### chapter 37
    harry        10
    quirrell     1

### chapter 38
    harry        24
    neville      4
    draco        3

### chapter 39
    harry        54
    dumbledore   18
    draco        1
    hermione     1

### chapter 40
    harry        11
    quirrell     5

### chapter 41
    draco        2
    harry        2

### chapter 42
    harry        22
    draco        6
    quirrell     1
    hermione     1

### chapter 43
    harry        26
    hermione     12
    quirrell     6
    dumbledore   2

### chapter 44
    dumbledore   2
    hermione     2
    harry        2

### chapter 45
    harry        24
    quirrell     4
    dumbledore   3
    hermione     1

### chapter 46
    harry        23
    dumbledore   7
    quirrell     5

### chapter 47
    draco        58
    harry        52
    quirrell     2
    dumbledore   1

### chapter 48
    harry        12
    hermione     10

### chapter 49
    harry        29
    quirrell     11

### chapter 50
    harry        11
    quirrell     1
    hermione     1

### chapter 51
    harry        21
    quirrell     9

### chapter 52
    harry        15

### chapter 53
    harry        5

### chapter 54
    harry        8

### chapter 55
    harry        25

### chapter 56
    harry        17
    dumbledore   4

### chapter 57
    harry        19
    dumbledore   2

### chapter 58
    harry        19
    quirrell     1

### chapter 59
    harry        17
    dumbledore   1

### chapter 60
    harry        3
    quirrell     2

### chapter 61
    dumbledore   2
    harry        1

### chapter 62
    harry        9
    mcgonagall   3
    dumbledore   3

### chapter 63
    harry        39
    draco        12
    snape        9
    neville      7
    hermione     4
    quirrell     1

### chapter 64

### chapter 65
    harry        20
    hermione     3
    quirrell     2

### chapter 66
    hermione     5
    harry        5
    neville      1

### chapter 67
    harry        11
    hermione     8
    neville      7
    draco        2

### chapter 68
    hermione     13
    dumbledore   6
    harry        6
    quirrell     3
    mcgonagall   1
    draco        1

### chapter 69
    hermione     17
    harry        9

### chapter 70
    hermione     17
    mcgonagall   4
    quirrell     2
    dumbledore   2
    harry        2

### chapter 71
    draco        4
    hermione     3
    harry        3
    quirrell     2

