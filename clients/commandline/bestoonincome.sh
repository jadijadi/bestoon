#!/bin/bash

source "$(dirname $0)"/bestoonconfig.sh

print_usage()
{
    echo "Use this script to submit income reports to ${BASE_URL}"
    echo "Usage: ${0} <Amount> <Description>. Eg:"
    echo "Usage: ${0} 1000 Donation"
}

# The script needs 2 arguments.
# The first argument should be a number
# The second argument should be a non-empty string
if [ ! $# -eq 2 -o -z "${1##*[!0-9]*}" -o -z "${2}" ]
then
    print_usage
    exit 1
fi


curl --data "token=$TOKEN&amount=$1&text=$2" $BASE_URL/submit/income/
