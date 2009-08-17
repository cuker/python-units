#!/usr/bin/env sh

ROOT=pypy

echo "Getting PyPy"
svn co http://codespeak.net/svn/pypy/dist@66797 $ROOT
echo "Patching PyPy"
patch -d $ROOT -p0 < patches
echo "Linking to 'units' module"
ln -s `pwd`/../units $ROOT/pypy/lib/units
echo "Run with" $ROOT"/pypy/bin/py.py"


