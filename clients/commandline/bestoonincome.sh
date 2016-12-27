#!/bin/bash

source config.sh

curl --data "token=$TOKEN&amount=$1&text=$2" $BASE_URL/submit/income/
