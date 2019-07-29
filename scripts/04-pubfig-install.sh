#!/bin/bash
set -u
MODNAME=$1

PKGPATH=`python -m site --user-site`
mkdir -p $PKGPATH/$MODNAME
touch $PKGPATH/$MODNAME/__init__.py
cp 04-pubfig.py $PKGPATH/$MODNAME/pubfig.py