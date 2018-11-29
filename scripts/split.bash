#!/bin/bash

mkdir out/img -p

# separate output
for i in {1..80}
do
    emacs -Q -batch log.txt --eval="(delete-non-matching-lines \"label $i \")" \
	  --eval="(write-file \"./out/$i.txt\")"
done

# remove empty files
for f in out/*.txt
do
    if [ ! -s $f ]
    then rm $f
    fi
done

# save graph images
for f in out/*.txt
do
    output=${f%.txt}.png
    output=out/img/${output##*out/}
    echo "Writing $output"
    gnuplot -e "set xrange [-3:7]; set yrange [-6:4]; set term png; set output \"$output\"; plot \"$f\" using 3:4 with dots, '' using 3:4:2 with labels"
done

# save whole graph
gnuplot -e "set xrange [-3:7]; set yrange [-6:4]; set term png; set output 'out/img/whole.png'; plot 'log.txt' using 3:4 with dots, '' using 3:4:2 with labels"
