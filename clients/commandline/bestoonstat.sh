#!/bin/bash

source config.sh

curl --data "token=$TOKEN" $BASE_URL/q/generalstat/
