#!/bin/bash

set -e

{

./scripts/setenv.jlabknl.sh

export CC=gcc
export CXX=g++

./scripts/xz.sh
./scripts/tar.sh
./scripts/gmp.sh
./scripts/mpfr.sh
./scripts/mpc.sh
./scripts/gcc.sh
./scripts/binutils.sh
./scripts/cmake.sh
./scripts/perl.sh
./scripts/openssl.sh
./scripts/libffi.sh
./scripts/zlib.sh
./scripts/openblas.sh
./scripts/python.sh
./scripts/python-packages.sh
./scripts/re2c.sh
./scripts/ninja.sh
./scripts/llvm-project.sh

export CC=
export CXX=

./scripts/fftw.sh
./scripts/fftwf.sh
./scripts/cuba.sh
./scripts/zlib.sh
./scripts/eigen.sh
./scripts/autoconf.sh
./scripts/automake.sh
./scripts/c-lime.sh
./scripts/hdf5.sh

./scripts/qlat.sh
./scripts/grid-tblum.knl.sh
./scripts/hadrons-tblum.sh
./scripts/grid.knl.sh
./scripts/gpt.knl.sh

} |& tee $prefix/log.build.txt
