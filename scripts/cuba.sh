#!/bin/bash

. scripts/conf.sh

name=Cuba

{

echo "!!!! build $name !!!!"

rm -rf $src_dir
mkdir -p $src_dir
cd $src_dir
tar xaf $distfiles/$name-*.tar.*

export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"

cd $name-*
./configure \
    --build="$(arch)" \
    --prefix=$prefix
make
make install

cd $wd
echo "!!!! $name build !!!!"

rm -rf $temp_dir || true

} |& tee $prefix/log.$name.txt
