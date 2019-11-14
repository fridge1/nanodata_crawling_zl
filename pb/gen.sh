#!/bin/sh
SRC_DIR=./src
DST_DIR=./

#PYTHON
#rm -fr $DST_DIR
mkdir -p $DST_DIR

for f in $(find $SRC_DIR -iname "*.proto"); do
    protoc -I=$SRC_DIR --python_out=$DST_DIR/ $f
done