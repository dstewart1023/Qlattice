#!/bin/bash

name=qmp

source qcore/set-prefix.sh $name

{ time {

    echo "!!!! build $name !!!!"

    source qcore/conf.sh ..

    rm -rf $src_dir || true
    mkdir -p $src_dir || true
    cd $src_dir
    time-run tar xzf $distfiles/$name-*.tar.gz

    rm -rf $build_dir || true
    mkdir -p $build_dir || true
    cd $build_dir

    export CFLAGS="$CFLAGS -fPIC"
    export CXXFLAGS="$CXXFLAGS -fPIC"

    time-run "$src_dir"/*"$name"*/configure \
        --with-qmp-comms-type=mpi \
        --prefix="$prefix" \
        CXX=$MPICXX CC=$MPICC

    time-run make -j$num_proc
    # time-run make check
    time-run make install

    mk-setenv.sh
    echo "!!!! $name build !!!!"
    rm -rf "$temp_dir" || true
} } 2>&1 | tee $prefix/log.$name.txt
