#!/bin/bash

source ./bestoonconfig.sh

curl --data "token=$TOKEN" $BASE_URL/q/generalstat/
