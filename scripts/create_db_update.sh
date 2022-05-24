#!/bin/bash

source ./db/version
i=$(($VERSION+1))

read -p 'Enter a filename: ' NAME
touch ./db/$(($i))_$NAME.py
SED_PARAM=s/VERSION=.*/VERSION=${i}/
sed -i "$SED_PARAM" ./db/version
echo "Migration file '$(($i))_$NAME.py' created"