#!/bin/bash
set -u

MODNAME=$1
MODPATH=`python -m site --user-site`

mkdir -p $MODPATH/$MODNAME
touch $MODPATH/$MODNAME/__init__.py
cp 04-pubfig.py $MODPATH/$MODNAME/pubfig.py