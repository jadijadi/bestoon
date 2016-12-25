#!/bin/bash

# please set these varialbes
TOKEN=1234567
BASE_URL=http://bestoon.ir

curl --data "token=$TOKEN&amount=$1&text=$2" $BASE_URL/submit/expense/
