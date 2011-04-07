#!/usr/bin/env fish

function halp
    echo "usage:  download-hpmor.fish [options] CHAPTER_NUM..." >&2
end
for opt in $argv; echo "$opt" | egrep -xq -e '--?h(e(lp?)?)?'; and halp; and exit 1; end


function fetch_hp_mor_chapter
    set -l i $argv[1]
    printf "Fetching $i... "
    if curl --fail --silent --url "http://www.fanfiction.net/s/5782108/$i/Harry_Potter_and_the_Methods_of_Rationality" -o "html/chapter-$i.html"
        printf "ok. Extracting story text... "
        # nb. doesn't deal well with unicode marks
        if xgrep -f "html/chapter-$i.html" "#storytext" > "txt/chapter-$i.html"
            echo "ok!"
        else
            echo "FAIL ($status)"
        end
    else
        echo "FAIL ($status)!"
    end
end

set -l start 64
set -l finish 71
if test "$start" -a "$start" -gt 0 -a "$finish" -a "$finish" -gt "$start"
    echo "Fetching all chapters between $start and $finish..."
    for i in (seq $start $finish)
        fetch_hp_mor_chapter $i
    end
end

if test "$argv"
    for i in $argv
        fetch_hp_mor_chapter $i
    end
end

# to get text block:
#
# xgrep -f $f "#storytext" > txt/$f
#
# Loopz: 
# for i in (seq $start $finish)
#     set -l f "chapter-$i.html"
#     xgrep -f $f "#storytext" > txt/$f
# end
