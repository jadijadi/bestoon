#!/bin/bash

source bestoonconfig.sh

AMOUNT=$1
shift 
TEXT=$*
if [ -z "$TEXT" ] ; then
    echo "
Error: parameters are required.

Usage:
    $0 Amount \"Descriptin of income\"
"
    exit 1       
fi

curl --data "token=$TOKEN&amount=$AMOUNT&text=$TEXT" $BASE_URL/submit/income/
