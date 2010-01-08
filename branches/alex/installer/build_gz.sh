#!/bin/bash
# This Script is used to build the tar.gz file

cd ..
# Clean up temporary files
find . -name \*.pyc | xargs rm -f
find . -name \*.py~ | xargs rm -f

# Get the Name 
dName="`grep -w "NAME = " src/mapConst.py`"
dName=${dName:8}
dName=${dName/%\"}

# Get the Version
dVer="`grep -w "VERSION = " src/mapConst.py`"
dVer=${dVer:11}
dVer=${dVer/%\"}

# Copy all the files to a temp location
mkdir -p ../temp/$dName-$dVer
cp -r * ../temp/$dName-$dVer
cd ../temp

# Remove some files
rm -r -f $dName-$dVer/common
find . -name \.svn | xargs rm -r -f

# Create the tar.gz file
tar czf ../$dName-$dVer.tar.gz $dName-$dVer

# Delete temp directory
cd ..
rm -r -f temp/


