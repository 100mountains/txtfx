#!/bin/bash


function aa_256()
{
    local o x=`tput op` y=`printf %$((${COLUMNS}-6))s`;
    for i in {0..256};
    do
        o=00$i;
        echo -e ${o:${#o}-3:3} `tputm "setaf $i" "setab $i"`${y// /=}$x;
    done
}
~                                                                                                                                                                               
c ()
{
    tput clear;
    pm "$TERM: [colors:`tput colors`/`tput pairs`]";
    RC=`tput op` L1=$(L '=' $(( ${COLUMNS} - 25 )));
    for i in `seq ${1:-0} ${2:-16}`;
    do
        o="  $i";
        echo -e " ${o:${#o}-3:3} `tput setaf $i;tput setab $i`${L1}${RC}";
    done
}
~                                                                                                                                                                               
~                                                                                                                                                                               
~                                                                                                                                                                               
~                                                                                                                                                                               
~                         
c
