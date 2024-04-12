#!/bin/bash
# Execute this script with options to show terminal colors.

# Displays usage information
function usage() {
    echo "Usage: $0 [option]"
    echo "Options:"
    echo "  1 - Run a function to display a set of colors."
    echo "  2 - Run a function to display an extended set of colors."
    echo "If no option is provided, nothing will be executed."
}

function L() {
    local char=$1
    local count=$2
    printf "%-${count}s" " " | tr ' ' "$char"
}

function aa_256() {
    tput clear
    local o x=$(tput op) y=$(printf %$((${COLUMNS}-6))s)
    for i in {0..256}; do
        o=00$i
        echo -e "${o:${#o}-3:3} $(tput setaf $i)$(tput setab $i)${y// /=}$x"
    done
}

function c() {
    tput clear
    echo "$TERM: [colors:$(tput colors)/$(tput pairs)]"
    local RC=$(tput op) L1=$(L '=' $(( ${COLUMNS} - 25 )))
    for i in $(seq ${1:-0} ${2:-16}); do
        local o="  $i"
        echo -e " ${o:${#o}-3:3} $(tput setaf $i;tput setab $i)${L1}${RC}"
    done
}

# Check command-line options
case "$1" in
    1)
        c
        ;;
    2)
        aa_256
        ;;
    *)
        usage
        exit 1
        ;;
esac
