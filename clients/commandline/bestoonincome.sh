#!/bin/bash

source "$(dirname $0)"/bestoonconfig.sh

print_usage()
{
    echo "Use this script to submit income reports to ${BASE_URL}"
    echo "Usage: ${0} <Amount> <Description>. Eg:"
    echo "Usage: ${0} 1000 Donation"
}

AMOUNT=$1
shift
TEXT=$*
if [ -z "$TEXT" ]; then
    print_usage
    exit 1
fi

curl --data "token=$TOKEN&amount=$AMOUNT&text=$TEXT" $BASE_URL/submit/income/
