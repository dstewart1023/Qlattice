#!/bin/bash

name=fftwf_mpi
pkgname=fftw

source qcore/set-prefix.sh $name

{ time {
    echo "!!!! build $name !!!!"
    source qcore/conf.sh ..

    rm -rf $src_dir || true
    mkdir -p $src_dir || true
    cd $src_dir
    tar xzf $distfiles/$pkgname-*.tar.gz

    cd $pkgname-*

    export CFLAGS="$CFLAGS -fPIC"
    export CXXFLAGS="$CXXFLAGS -fPIC"

    ./configure \
        --prefix=$prefix \
        --enable-float \
        --enable-mpi \
        --enable-shared

    make -j$num_proc
    make install

    mk-setenv.sh
    echo "!!!! $name build !!!!"
    rm -rf $temp_dir || true
} } 2>&1 | tee $prefix/log.$name.txt
