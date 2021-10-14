#!/bin/bash

./scripts/setenv.sh

./scripts/xz.sh
./scripts/tar.sh
./scripts/gmp.sh
./scripts/mpfr.sh
./scripts/mpc.sh
./scripts/gcc.sh
./scripts/openmpi.sh
./scripts/openssl.sh
./scripts/libffi.sh
./scripts/python.sh
./scripts/python-packages.sh

./scripts/fftw.sh
./scripts/fftwf.sh
./scripts/cuba.sh
./scripts/zlib.sh
./scripts/eigen.sh
./scripts/qlat.sh

./scripts/c-lime.sh
./scripts/grid-avx2.sh
./scripts/gpt.sh