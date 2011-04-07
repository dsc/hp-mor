#! /bin/bash

source ~/scripts/toolbox.sh

VERBOSE=""

function halp () {
    cat >&2 <<-HALP
MoR Downloader -- Scrapes FanFiction.net for HP:MoR text.

Usage:     $( basename $0 ) [options] [CHAPTER_NUM...]

Arguments:
    CHAPTER_NUM		Optional. Individual chapter numbers to grab.

Options:
    -h				Displays this help.
    -s				Start of chapter range to DL (inclusive); requires --finish.
    -f				End of chapter range to DL (inclusive); requires --start.
HALP
}

SHIFT=0
function incshift () { SHIFT=$(( $SHIFT + ${1:-1} )); }
function log () { test "$VERBOSE" && return 0;  echo && echo "$*"; return 0; }
function fail () { echo "PREDICTABLE FAILURE. $1" >&2; exit 1; }
function join () { sep="$1"; printf "$2"; shift 2; for a in $*; do printf "$sep$a"; done; echo; }

for opt in $*; do echo $opt | egrep -xq -e '--?h(e(lp?)?)?' && { halp; exit 0; }; done
while getopts ":vb:s:f:" opt; do
    case $opt in
        v ) VERBOSE="-v";   incshift ;;
        s ) START=$OPTARG;  incshift 2 ;;
        f ) FINISH=$OPTARG; incshift 2 ;;
        * ) fail "Unknown option: $OPTARG" ;;
    esac
done
shift $SHIFT

function fetch_hp_mor_chapter () {
    printf "Fetching $1... "
    if curl --fail --silent --url "http://www.fanfiction.net/s/5782108/$1/Harry_Potter_and_the_Methods_of_Rationality" -o "html/chapter-$1.html"; then
        echo "ok."
        # printf "ok. Extracting story text... "
        # nb. doesn't deal well with unicode marks
        # if xgrep -f "html/chapter-$1.html" "#storytext" > "txt/chapter-$1.html"; then
        #     echo "ok!"
        # else
        #     echo "FAIL ($status)"
        # fi
    else
        echo "FAIL ($?)!"
    fi
}

if test "$START" -a ( "$START" -gt 0 ) -a "$FINISH" -a ( "$FINISH" -gt "$START" ); then
    echo "Fetching all chapters between $START and $FINISH..."
    for i in $(seq $start $finish); do
        fetch_hp_mor_chapter $i
    done
fi

if test "$*"; then
    for i in $*; do
        fetch_hp_mor_chapter $i
    done
fi
