#!/bin/bash

name=python-pip

source qcore/set-prefix.sh

{ time {
    echo "!!!! build $name !!!!"
    source qcore/conf.sh .

    find ~/.cache/pip/wheels -type f || true
    rm -rfv ~/.cache/pip/wheels || true

    opts="--verbose --no-index --no-build-isolation --no-cache-dir -f $distfiles/python-packages"

    time pip3 install $opts wheel
    time pip3 uninstall setuptools -y
    time pip3 install $opts setuptools
    time pip3 install $opts --upgrade pip

    echo "!!!! $name build !!!!"
    rm -rf $temp_dir || true
} } 2>&1 | tee $prefix/log.$name.txt
