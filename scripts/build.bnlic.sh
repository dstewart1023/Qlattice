#!/bin/bash

set -e

{

./scripts/setenv.bnlic.sh

./scripts/tar.sh

./scripts/fftw_mpi.sh
./scripts/fftwf_mpi.sh
./scripts/cuba.sh
./scripts/zlib.sh
./scripts/eigen.sh
./scripts/qlat.sh

./scripts/c-lime.sh
./scripts/grid.avx2.sh
./scripts/gpt.sh

} |& tee $prefix/log.build.txt
